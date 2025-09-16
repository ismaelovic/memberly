from pydantic import BaseModel
from typing import Optional


class CommunicationBase(BaseModel):
    type: str  # email, sms, push
    content: str
    status: Optional[str] = None


class CommunicationCreate(CommunicationBase):
    member_id: int


class CommunicationResponse(CommunicationBase):
    id: int
    member_id: int

    class Config:
        from_attributes = True
