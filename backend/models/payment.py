import enum
from sqlalchemy import BIGINT, ForeignKey, NUMERIC
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
import datetime


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    membership_id: Mapped[BIGINT] = mapped_column(
        ForeignKey("memberships.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tenant_id: Mapped[BIGINT] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    amount: Mapped[int] = mapped_column(NUMERIC, nullable=False)
    payment_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow, nullable=False
    )

    stripe_subscription_id: Mapped[str] = mapped_column(nullable=False)
    stripe_customer_id: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    stripe_currency: Mapped[str] = mapped_column(nullable=False)
    stripe_period_start: Mapped[int] = mapped_column(BIGINT, nullable=False)
    stripe_period_end: Mapped[int] = mapped_column(BIGINT, nullable=False)
    stripe_invoice_id: Mapped[str] = mapped_column(nullable=False)
    stripe_customer_email: Mapped[str] = mapped_column(nullable=False)

    membership = relationship("Membership", back_populates="payments")
