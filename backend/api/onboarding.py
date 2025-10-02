from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from uuid import uuid4
from datetime import datetime as dt, timedelta
from ..db.session import get_db
from ..models.tenant import OnboardingToken
from ..models.subscriptions import SubscriptionPlan
from ..models.tenant import Tenant

router = APIRouter()


# Generate Onboarding Token
@router.post("/api/system-admin/generate-tenant-link")
def generate_tenant_link(db: Session = Depends(get_db)):
    token = str(uuid4())
    expiration_date = dt.utcnow() + timedelta(days=1)  # Token valid for 1 day

    onboarding_token = OnboardingToken(
        token=token,
        expires_at=expiration_date,
        used=False,
    )
    db.add(onboarding_token)
    db.commit()
    db.refresh(onboarding_token)

    link = f"http://localhost:3000/onboard?token={token}"
    return {"link": link}


# Validate Onboarding Token
@router.post("/api/system-admin/validate-onboarding")
def validate_onboarding(token: str, db: Session = Depends(get_db)):
    onboarding_token = (
        db.query(OnboardingToken).filter(OnboardingToken.token == token).first()
    )

    if not onboarding_token:
        raise HTTPException(status_code=400, detail="Missing token")

    # Fixing the comparison issue
    if onboarding_token.expires_at < func.now().execute().scalar():
        raise HTTPException(status_code=400, detail="Invalid or expired token provided")

    if onboarding_token.used:
        raise HTTPException(status_code=400, detail="Token already used")

    # Mark token as used
    onboarding_token.used = True
    db.commit()

    return {"message": "Token is valid"}


# Create Subscription Plan
@router.post("/api/onboarding/subscription-plan")
def create_subscription_plan(
    tenant_id: int,
    name: str,
    description: str,
    price: float,
    duration_months: int,
    is_active: bool,
    is_popular: bool,
    features: list,
    db: Session = Depends(get_db),
):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    subscription_plan = SubscriptionPlan(
        tenant_id=tenant_id,
        name=name,
        description=description,
        price=price,
        duration_months=duration_months,
        is_active=is_active,
        is_popular=is_popular,
        features=features,
    )
    db.add(subscription_plan)
    db.commit()
    db.refresh(subscription_plan)

    return {
        "message": "Subscription plan created successfully",
        "plan_id": subscription_plan.id,
    }


# Retrieve Subscription Plans for a Tenant
@router.get("/api/onboarding/subscription-plans/{tenant_id}")
def get_subscription_plans(tenant_id: int, db: Session = Depends(get_db)):
    subscription_plans = (
        db.query(SubscriptionPlan).filter(SubscriptionPlan.tenant_id == tenant_id).all()
    )
    if not subscription_plans:
        raise HTTPException(
            status_code=404, detail="No subscription plans found for this tenant"
        )

    return subscription_plans
