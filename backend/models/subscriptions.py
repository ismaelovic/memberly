from sqlalchemy import BIGINT, NUMERIC, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base
import datetime


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tenant_id: Mapped[BIGINT] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column(NUMERIC, nullable=False)
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
