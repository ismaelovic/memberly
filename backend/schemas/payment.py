from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional


class PaymentBase(BaseModel):
    amount: float
    payment_date: datetime


class PaymentCreate(PaymentBase):
    membership_id: int
    tenant_id: int
    stripe_customer_id: str
    stripe_subscription_id: str
    stripe_currency: str
    stripe_period_start: int
    stripe_period_end: int
    stripe_invoice_id: str
    stripe_customer_email: Optional[str] = None
    status: str

    class Config:
        from_attributes = True

    @validator("stripe_customer_email")
    def validate_email(cls, v):
        if v and "@" not in v:
            raise ValueError("Invalid email address")
        return v

    @validator("stripe_customer_id")
    def validate_stripe_customer_id(cls, v):
        if not v.startswith("cus_"):
            raise ValueError("Invalid stripe_customer_id format")
        return v

    @validator("stripe_subscription_id")
    def validate_stripe_subscription_id(cls, v):
        if not v.startswith("sub_"):
            raise ValueError("Invalid stripe_subscription_id format")
        return v

    @validator("stripe_invoice_id")
    def validate_stripe_invoice_id(cls, v):
        if not v.startswith("in_"):
            raise ValueError("Invalid stripe_invoice_id format")
        return v

    @validator("status")
    def validate_status(cls, v):
        if not v in [
            "paid",
            "draft",
            "failed",
            "pending",
            "void",
            "uncollectible",
            "open",
        ]:
            raise ValueError("Invalid status format, check Stripe documentation")
        return v


class CheckoutSessionRequest(BaseModel):
    subscription_plan_id: int
    email: str
    membership_id: int  # Add membership_id to the request model
