from pydantic import BaseModel
from typing import Optional


class PaymentBase(BaseModel):
    amount: float
    status: str
    method: Optional[str] = None
    transaction_id: Optional[str] = None


class PaymentCreate(PaymentBase):
    member_id: int


class PaymentResponse(PaymentBase):
    id: int
    member_id: int

    class Config:
        from_attributes = True
