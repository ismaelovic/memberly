from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base
import datetime


class Membership(Base):
    __tablename__ = "memberships"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    member_id: Mapped[int] = mapped_column(
        ForeignKey("member_profile.id", ondelete="CASCADE"), nullable=False, index=True
    )
    plan_id: Mapped[int] = mapped_column(
        ForeignKey("subscription_plans.id"), nullable=False, index=True
    )
    adjusted_price: Mapped[float] = mapped_column(nullable=True)
    start_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow
    )
    end_date: Mapped[datetime.datetime] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)

    member = relationship("MemberProfile", back_populates="memberships")
    plan = relationship("SubscriptionPlan", back_populates="memberships")
    payments = relationship("Payment", back_populates="membership")


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    duration_months: Mapped[int] = mapped_column(
        nullable=False
    )  # Duration of the plan in months
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_popular: Mapped[bool] = mapped_column(nullable=False, default=False)
    features: Mapped[list] = mapped_column(
        JSONB, nullable=False
    )  # JSON field for subscription features as a list
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

    tenant = relationship("Tenant", back_populates="subscription_plans")
    memberships = relationship("Membership", back_populates="plan")
