from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.schemas.payment import PaymentCreate, CheckoutSessionRequest
from backend.models.payment import Payment
from backend.models.membership import Membership
from backend.models.subscriptions import SubscriptionPlan
from datetime import datetime

# Placeholder for Stripe integration
import stripe
from backend.core.logging import logger
from backend.core.config import settings
import json
from backend.services.stripe_helper import (
    handle_checkout_session_completed,
    handle_invoice_payment_succeeded,
    handle_invoice_payment_failed,
)

router = APIRouter()


@router.post("/payments")
def process_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    pass


@router.get("/payments")
def list_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()


@router.get("/payments/{id}")
def get_payment(id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.get("/payments/membership/{id}")
def get_payments_by_membership(id: int, db: Session = Depends(get_db)):
    payments = db.query(Payment).filter(Payment.membership_id == id).all()
    return payments


@router.post("/stripe/create-checkout-session")
def create_checkout_session(
    request: CheckoutSessionRequest,
    db: Session = Depends(get_db),
):
    stripe.api_key = settings.stripe_api_key

    # Fetch subscription plan details from the database
    subscription_plan = (
        db.query(SubscriptionPlan)
        .filter(SubscriptionPlan.id == request.subscription_plan_id)
        .first()
    )
    if not subscription_plan:
        raise HTTPException(status_code=404, detail="Subscription plan not found")

    # Validate membership_id
    membership = (
        db.query(Membership).filter(Membership.id == request.membership_id).first()
    )
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")

    try:
        # Create a Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=request.email,
            # customer=existing_stripe_customer_id, # Replace with the actual Stripe Customer ID
            # client_reference_id=str(your_internal_user_id), # Or your internal subscription ID
            metadata={
                "plan_name": subscription_plan.name,
                "membership_id": str(request.membership_id),
                "signup_source": "web_app",
            },
            line_items=[
                {
                    "price_data": {
                        "currency": "dkk",
                        "product_data": {
                            "name": subscription_plan.name,
                        },
                        "unit_amount": int(subscription_plan.price),  # Convert to cents
                        "recurring": {
                            "interval": "month",  # Set the billing interval (e.g., "month" or "year")
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="subscription",
            locale="da",  # Set checkout language to Danish
            success_url=f"{settings.frontend_base_url}/handle_stripe?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.frontend_base_url}/handle_stripe?session_id={{CHECKOUT_SESSION_ID}}",
        )

        return {"checkoutUrl": checkout_session.url}

    except Exception as e:
        print(f"Error creating Stripe Checkout Session: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to create Stripe Checkout Session"
        )


@router.post("/stripe/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    stripe.api_key = settings.stripe_api_key
    endpoint_secret = settings.stripe_signing_secret  # Add this to your settings

    try:
        # Cache the body by reading it once
        payload = await request.body()
        sig_header = request.headers.get("stripe-signature")

        # Use the cached payload for constructing the event
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        print(f"Error verifying Stripe webhook: {e}")
        raise HTTPException(status_code=400, detail="Invalid Stripe webhook payload")

    event_type = event["type"]
    event_data = event["data"]["object"]

    try:
        if event_type == "checkout.session.completed":
            handle_checkout_session_completed(event_data, db)
        elif event_type == "invoice.payment_succeeded":
            handle_invoice_payment_succeeded(event_data, db)
        elif event_type == "invoice.payment_failed":
            handle_invoice_payment_failed(event_data, db)
        else:
            # Log unhandled events to a JSON file for inspection
            unhandled_event = {
                "event_type": event_type,
                # "event_data": event_data,
                "timestamp": datetime.utcnow().isoformat(),
            }
            with open("unhandled_events.json", "a") as f:
                f.write(json.dumps(unhandled_event) + "\n")
    except Exception as e:
        print(f"Error handling event {event_type}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error handling event {event_type}"
        )

    return {"status": "success"}
