import stripe
from backend.models.payment import Payment
from datetime import datetime
from sqlalchemy.orm import Session
from backend.core.logging import logger
from backend.core.config import settings

stripe.api_key = settings.stripe_api_key


def handle_checkout_session_completed(event_data, db: Session):
    subscription_id = event_data.get("subscription")
    if not subscription_id:
        raise ValueError("Subscription ID not found in event data.")

    # Retrieve subscription and invoice details
    subscription = stripe.Subscription.retrieve(subscription_id)
    latest_invoice_id = subscription["latest_invoice"]
    invoice = stripe.Invoice.retrieve(latest_invoice_id)

    # Create a new payment record
    new_payment = Payment(
        membership_id=event_data["metadata"]["membership_id"],
        tenant_id=settings.default_tenant,  # TODO: Replace with actual tenant ID logic
        amount=invoice["amount_paid"] / 100,
        payment_date=datetime.utcnow(),
        stripe_subscription_id=subscription_id,
        stripe_customer_id=subscription["customer"],
        status=subscription["status"],
        stripe_currency=invoice["currency"],
        stripe_period_start=invoice["period_start"],
        stripe_period_end=invoice["period_end"],
        stripe_invoice_id=latest_invoice_id,
        stripe_customer_email=event_data["customer_email"],
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    print(f"Payment created for subscription: {subscription_id}")


def handle_invoice_payment_succeeded(event_data, db: Session):
    invoice = event_data
    print(f"Invoice payment succeeded: {invoice['id']}")

    # Update payment record or create a new one
    existing_payment = (
        db.query(Payment).filter_by(stripe_invoice_id=invoice["id"]).first()
    )
    if existing_payment:
        existing_payment.status = invoice["status"]
        db.commit()
        print(f"Updated payment status for invoice: {invoice['id']}")
    else:
        print(f"No payment record found for invoice: {invoice['id']}")


def handle_invoice_payment_failed(event_data, db: Session):
    invoice = event_data
    print(f"Invoice payment failed: {invoice['id']}")

    # Update payment record or notify the user
    existing_payment = (
        db.query(Payment).filter_by(stripe_invoice_id=invoice["id"]).first()
    )
    if existing_payment:
        existing_payment.status = invoice["status"]
        db.commit()
        print(f"Updated payment status for failed invoice: {invoice['id']}")
    else:
        print(f"No payment record found for failed invoice: {invoice['id']}")
