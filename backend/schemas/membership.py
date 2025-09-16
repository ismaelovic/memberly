from pydantic import BaseModel
from typing import Optional


class MembershipBase(BaseModel):
    plan_name: str
    price: float
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_active: Optional[bool] = True


class MembershipCreate(MembershipBase):
    member_id: int


class MembershipUpdate(MembershipBase):
    pass


class MembershipResponse(MembershipBase):
    id: int
    member_id: int

    class Config:
        from_attributes = True
