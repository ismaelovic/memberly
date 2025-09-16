from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import Base
import datetime


class Membership(Base):
    __tablename__ = "memberships"
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    plan_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    member = relationship("Member", back_populates="memberships")
