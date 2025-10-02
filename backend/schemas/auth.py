from pydantic import BaseModel, Field, validator
from backend.models.user import MemberGender
from datetime import date


class LoginRequest(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True

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


class RegisterMemberRequest(RegisterRequest):
    subscription_plan_id: int


class ChangePasswordRequest(BaseModel):
    user_id: int
    old_password: str
    new_password: str
