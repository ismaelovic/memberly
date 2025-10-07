from pydantic import BaseModel, Field, validator
from datetime import date
import enum


class Role(enum.Enum):
    SYSTEM_ADMIN = "system_admin"
    TENANT_ADMIN = "tenant_admin"
    STAFF = "staff"
    MEMBER = "member"


class MemberState(enum.Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    SUSPENDED = "suspended"
    PAUSED = "paused"
    PENDING = "pending"


class MemberGender(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class LoginRequest(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

    @validator("email")
    def validate_email(cls, v):
        if v and "@" not in v:
            raise ValueError("Invalid email address")
        return v

    @validator("password")
    def validate_password(cls, v):
        if not v or len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v


class RegisterRequest(LoginRequest):
    first_name: str
    last_name: str
    address: str
    phone: str
    zip_code: str
    date_of_birth: date
    gender: MemberGender
    state: MemberState = Field(default=MemberState.PENDING)
    role: Role = Field(default=Role.MEMBER)


class RegisterMemberRequest(RegisterRequest):
    tenant_id: int
    subscription_plan_id: int


class ChangePasswordRequest(BaseModel):
    user_id: int
    old_password: str
    new_password: str
