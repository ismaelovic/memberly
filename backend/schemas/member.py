from pydantic import BaseModel
from typing import Optional


class MemberBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = True


class MemberCreate(MemberBase):
    pass


class MemberUpdate(MemberBase):
    pass


class MemberResponse(MemberBase):
    id: int

    class Config:
        from_attributes = True
