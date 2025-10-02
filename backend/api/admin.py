from fastapi import APIRouter, Depends, HTTPException, Request

from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.models.tenant import Tenant
from backend.models.user import MemberAuth
from backend.models.membership import Membership
from backend.models.subscriptions import SubscriptionPlan
from backend.schemas.admin import OnboardingCompleteRequest
from pydantic import ValidationError

router = APIRouter()


@router.get("/system-admin/stats")
def get_system_admin_stats(db: Session = Depends(get_db)):
    try:
        tenants_count = db.query(Tenant).count()
        users_count = db.query(MemberAuth).count()
        active_subscriptions_count = (
            db.query(SubscriptionPlan)
            .filter(SubscriptionPlan.is_active == True)
            .count()
        )
        active_memberships_count = (
            db.query(Membership).filter(Membership.is_active == True).count()
        )

        return {
            "tenants": tenants_count,
            "users": users_count,
            "activeSubscriptions": active_subscriptions_count,
            "activeMemberships": active_memberships_count,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {str(e)}")


@router.post("/system-admin/generate-tenant-link")
def generate_tenant_link():
    # Placeholder logic for generating a tenant onboarding link
    # Replace with actual implementation
    import uuid

    unique_link = f"https://yourapp.com/onboard/{uuid.uuid4()}"
    return {"link": unique_link}


@router.post("/onboarding/complete")
async def complete_onboarding(
    request: OnboardingCompleteRequest, db: Session = Depends(get_db)
):
    try:
        # print(await request.body())
        user = request.user
        tenant = request.tenant
        subscriptions = request.subscriptions

        print(
            "Incoming Request Body:", user, tenant, subscriptions
        )  # Log the request body
        # Validate the request body against the schema
        validated_data = OnboardingCompleteRequest(**request.dict())
        return {"message": "Success"}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=f"Validation error: {ve.json()}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to complete onboarding: {str(e)}"
        )

    # return {"message": "Onboarding completed successfully"}
