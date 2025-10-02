from pydantic import BaseModel
from typing import Optional, List
from pydantic import BaseModel, Field


class SubscriptionsBase(BaseModel):
    name: str = Field(..., max_length=100)
    price: float = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=500)
    duration_months: Optional[int] = Field(None, gt=0)
    is_popular: Optional[bool] = Field(False)
    is_active: Optional[bool] = Field(True)
    features: Optional[List[str]] = Field(None)


class SubscriptionCreate(SubscriptionsBase):
    pass


class SubscriptionUpdate(SubscriptionsBase):
    plan_id: int
