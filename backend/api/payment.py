from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.schemas.payment import PaymentCreate, PaymentResponse
from backend.models.payment import Payment, PaymentStatus
from backend.models.membership import SubscriptionPlan, Membership
from typing import List
from datetime import datetime

# Placeholder for Stripe integration
import stripe
from backend.core.logging import logger
from backend.core.config import settings

router = APIRouter()


@router.post("/payments", response_model=PaymentResponse)
def process_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    # Example Stripe integration logic
    try:
        stripe.api_key = "your-stripe-secret-key"
        charge = stripe.Charge.create(
            amount=int(payment.amount * 100),  # Convert to cents
            currency="usd",
            source="tok_visa",  # Replace with actual token from frontend
            description=f"Payment for member {payment.member_id}",
        )
        payment.status = "succeeded" if charge["status"] == "succeeded" else "failed"
        payment.transaction_id = charge["id"]
    except Exception as e:
        logger.error(f"Error processing payment: {e}")
        raise HTTPException(
            status_code=400, detail=f"Payment processing error: {str(e)}"
        )

    new_payment = Payment(**payment.dict())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


@router.get("/payments", response_model=List[PaymentResponse])
def list_payments(db: Session = Depends(get_db)):
    return db.query(Payment).all()


@router.post("/stripe/create-checkout-session")
def create_checkout_session(
    subscription_plan_id: int,
    email: str,
    db: Session = Depends(get_db),
):
    stripe.api_key = settings.stripe_api_key

    # Fetch subscription plan details from the database
    subscription_plan = (
        db.query(SubscriptionPlan)
        .filter(SubscriptionPlan.id == subscription_plan_id)
        .first()
    )
    if not subscription_plan:
        raise HTTPException(status_code=404, detail="Subscription plan not found")

    try:
        # Create a Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=email,
            line_items=[
                {
                    "price_data": {
                        "currency": "dkk",
                        "product_data": {
                            "name": subscription_plan.name,
                        },
                        "unit_amount": int(subscription_plan.price),  # Convert to cents
                    },
                    "quantity": 1,
                }
            ],
            mode="subscription",
            success_url=f"{settings.frontend_base_url}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.frontend_base_url}/register",
        )

        # Create Membership entry
        new_membership = Membership(
            user_email=email,
            subscription_plan_id=subscription_plan_id,
            start_date=datetime.utcnow(),
        )
        db.add(new_membership)
        db.commit()
        db.refresh(new_membership)

        # Record payment details in the Payment table
        new_payment = Payment(
            user_email=email,
            subscription_plan_id=subscription_plan_id,
            amount=subscription_plan.price,
            status="pending",  # Initial status, to be updated by webhook
            transaction_id=checkout_session.id,  # Use Stripe session ID as transaction ID
        )
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)

        return {"checkoutUrl": checkout_session.url}

    except Exception as e:
        logger.error(f"Error creating Stripe Checkout Session: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to create Stripe Checkout Session"
        )


@router.post("/stripe/webhook")
def stripe_webhook(payload: dict, db: Session = Depends(get_db)):
    stripe.api_key = (
        "your-stripe-secret-key"  # Replace with your actual Stripe secret key
    )

    # Verify the webhook signature
    sig_header = payload.get("stripe-signature")
    endpoint_secret = (
        "your-webhook-signing-secret"  # Replace with your actual endpoint secret
    )

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=endpoint_secret
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Retrieve the payment and update its status
        payment = (
            db.query(Payment)
            .filter(Payment.stripe_payment_intent_id == session["id"])
            .first()
        )
        if payment:
            payment.status = PaymentStatus.COMPLETED  # Use the correct enum value
            db.commit()
            db.refresh(payment)

    return {"status": "success"}
