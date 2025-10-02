import datetime
from sqlalchemy import (
    DateTime,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=True)
    logo: Mapped[str] = mapped_column(nullable=True)  # URL to the logo image

    members = relationship("MemberProfile", back_populates="tenant")
    subscription_plans = relationship("SubscriptionPlan", back_populates="tenant")


class OnboardingToken(Base):
    __tablename__ = "onboarding_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    token: Mapped[str] = mapped_column(nullable=False, unique=True)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    used: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Removed tenant_id as the receiver of the link creates the tenant
