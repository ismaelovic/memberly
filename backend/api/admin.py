from fastapi import APIRouter, Depends, HTTPException, Request

from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.models.tenant import Tenant, create_tenant
from backend.models.user import MemberAuth, MemberProfile, create_user
from backend.models.membership import Membership
from backend.models.subscriptions import SubscriptionPlan, create_subscriptions
from backend.schemas.admin import OnboardingCompleteRequest
from datetime import datetime, timedelta
import uuid
from backend.models.tenant import OnboardingToken
from backend.utils.token_validation import validate_token
from backend.core.config import settings

router = APIRouter(prefix="/admin")


@router.get("/tenant/stats/")
def get_tenant_admin_stats(db: Session = Depends(get_db)):
    try:
        tenant = (
            settings.default_tenant
        )  # TODO: Replace with dynamic tenant when logic is setup.
        users_count = (
            db.query(MemberProfile).filter(MemberProfile.tenant_id == tenant).count()
        )
        active_subscriptions_count = (
            db.query(SubscriptionPlan)
            .filter(SubscriptionPlan.is_active == True)
            .filter(SubscriptionPlan.tenant_id == tenant)
            .count()
        )
        active_memberships_count = (
            db.query(Membership)
            .join(SubscriptionPlan, Membership.plan_id == SubscriptionPlan.id)
            .filter(SubscriptionPlan.tenant_id == tenant)
            .filter(Membership.is_active == True)
            .count()
        )

        return {
            # "tenants": tenants_count,
            "users": users_count,
            "activeSubscriptions": active_subscriptions_count,
            "activeMemberships": active_memberships_count,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {str(e)}")


@router.get("/system/stats")
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


@router.post("/system/generate-tenant-link")
def generate_tenant_link(db: Session = Depends(get_db)):
    # Generate a unique token
    token = str(uuid.uuid4())
    expiration = datetime.utcnow() + timedelta(days=7)  # Token valid for 7 days

    # Save the token in the database
    invite = OnboardingToken(token=token, expires_at=expiration, used=False)
    db.add(invite)
    db.commit()

    # Generate the onboarding link
    unique_link = f"{settings.frontend_base_url}/onboard-tenant/{token}"
    return {"link": unique_link}


@router.get("/onboard")
def onboarding_get():
    raise HTTPException(status_code=403, detail="Missing token")


@router.get("/onboard/{token}")
def onboarding_token_get(token: str, db: Session = Depends(get_db)):
    """
    Validate the onboarding token when the user accesses the onboarding page.
    If valid, allow the user to proceed; otherwise, raise an error.
    """
    try:
        # Validate the token using the utility
        validate_token(db, token)

        # If valid, return a success message
        return {
            "message": "Token is valid. You may proceed with onboarding.",
            "proceed": True,
        }
    except HTTPException as e:
        # If invalid, return an error message
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/onboard/{token}")
async def onboarding_token_post(
    token: str, request: OnboardingCompleteRequest, db: Session = Depends(get_db)
):
    """
    Complete the onboarding process by saving user, tenant, and subscription data.
    Ensure all actions are handled atomically.
    """
    # Validate the token
    if not validate_token(db, token):
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    try:
        tenant = create_tenant(db, request.tenant)
        create_user(db, request.user, tenant_id=tenant.id)
        create_subscriptions(db, request.subscriptions, tenant_id=tenant.id)

        # Mark the token as used
        db.query(OnboardingToken).filter(OnboardingToken.token == token).update(
            {"used": True}
        )
        db.commit()

        return {
            "message": f"Onboarding completed successfully. {tenant.name} created with admin {request.user.first_name} {request.user.last_name}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to complete onboarding: {str(e)}"
        )
