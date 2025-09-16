from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.schemas.payment import PaymentCreate, PaymentResponse
from backend.models.payment import Payment
from typing import List

# Placeholder for Stripe integration
import stripe
from backend.core.logging import logger

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
