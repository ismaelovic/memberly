from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
import datetime


class Communication(Base):
    __tablename__ = "communications"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    member_id = Column(
        Integer, ForeignKey("member_profile.id"), nullable=False, index=True
    )
    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    type = Column(String, nullable=False)  # email, sms, push
    content = Column(String, nullable=False)
    status = Column(String)
    sent_at = Column(DateTime, default=datetime.datetime.utcnow)

    member = relationship("Member", back_populates="communications")
