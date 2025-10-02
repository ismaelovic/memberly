from pydantic import BaseModel, Field, validator
from backend.api.subscriptions import SubscriptionCreate
from backend.schemas.auth import RegisterRequest
from backend.schemas.tenant import TenantCreate
from typing import List


class OnboardingCompleteRequest(BaseModel):
    user: RegisterRequest
    tenant: TenantCreate
    subscriptions: List[SubscriptionCreate]
