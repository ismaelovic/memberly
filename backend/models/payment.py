import enum
from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
import datetime


class PaymentStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    member_id: Mapped[int] = mapped_column(
        ForeignKey("member_profile.id", ondelete="CASCADE"), nullable=False, index=True
    )
    membership_id: Mapped[int] = mapped_column(
        ForeignKey("memberships.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    amount: Mapped[float] = mapped_column(nullable=False)
    payment_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow, nullable=False
    )
    stripe_payment_intent_id: Mapped[str] = mapped_column(nullable=False)
    stripe_charge_id: Mapped[str] = mapped_column(nullable=True)
    stripe_customer_id: Mapped[str] = mapped_column(nullable=False)
    stripe_subscription_id: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[PaymentStatus] = mapped_column(nullable=False, default="pending")
    currency: Mapped[str] = mapped_column(nullable=False, default="dkk")

    membership = relationship("Membership", back_populates="payments")
    member = relationship("MemberProfile", back_populates="payments")
