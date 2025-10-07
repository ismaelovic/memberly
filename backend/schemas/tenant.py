from typing import Optional
from pydantic import BaseModel, Field, validator


class TenantBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Tenant name")
    address: str = Field(..., min_length=1, description="Tenant address")
    phone: str
    logo: Optional[str] = Field(None, description="URL to the tenant's logo")

    class Config:
        from_attributes = True

    @validator("phone")
    def validate_phone(cls, value):
        if not len(value) == 8:
            raise ValueError("Phone number must be exactly 8 characters long")
        return value


class TenantCreate(TenantBase):
    pass  # Add fields specific to creation if needed


class TenantResponse(TenantBase):
    id: int  # Include fields returned by the database
