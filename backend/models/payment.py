from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import Base
import datetime


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    payment_date = Column(DateTime, default=datetime.datetime.utcnow)
    method = Column(String)
    transaction_id = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    member = relationship("Member", back_populates="payments")
