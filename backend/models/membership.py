from sqlalchemy import BIGINT, NUMERIC, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base
import datetime


class Membership(Base):
    __tablename__ = "memberships"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    member_id: Mapped[BIGINT] = mapped_column(
        ForeignKey("member_profile.id", ondelete="CASCADE"), nullable=False, index=True
    )
    plan_id: Mapped[BIGINT] = mapped_column(
        ForeignKey("subscription_plans.id"), nullable=False, index=True
    )
    adjusted_price: Mapped[int] = mapped_column(NUMERIC, nullable=True)
    start_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow, nullable=False
    )
    end_date: Mapped[datetime.datetime] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    member = relationship("MemberProfile", back_populates="memberships")
    plan = relationship("SubscriptionPlan", back_populates="memberships")
    payments = relationship("Payment", back_populates="membership")
