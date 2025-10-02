from fastapi import APIRouter, Response, Request, HTTPException, Depends
from datetime import timedelta, datetime, date
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from backend.models.tenant import Tenant

from backend.db.session import get_db
from backend.models.user import (
    MemberAuth,
    MemberProfile,
    MemberState,
    MemberGender,
    Role,
)
from backend.models.membership import Membership
from backend.models.subscriptions import SubscriptionPlan
from backend.schemas.auth import (
    LoginRequest,
    RegisterMemberRequest,
    ChangePasswordRequest,
)
from backend.core.security import create_access_token, verify_password, hash_password
from backend.core.config import settings
from backend.core.logging import logger

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.get("/auth/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(MemberAuth).all()
    return {"status": "success", "users": users}


@router.post("/auth/login")
def login(
    response: Response,
    login_request: LoginRequest,
    db=Depends(get_db),
):
    user = db.query(MemberAuth).filter(MemberAuth.email == login_request.email).first()
    if not user or not verify_password(login_request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.email},
        role=user.role,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        samesite="strict",
    )
    return {
        "message": "Login successful",
        "member_auth_id": user.id,
        "role": user.role.value,
    }


@router.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}


@router.get("/auth/profile/{user_id}")
def get_profile(user_id: int, request: Request, db: Session = Depends(get_db)):
    # token = request.cookies.get("access_token")
    # if not token:
    #     raise HTTPException(status_code=401, detail="Not authenticated")
    # Token validation logic here (omitted for brevity)
    # Assuming we have extracted the user's email from the token
    user = (
        db.query(MemberProfile).filter(MemberProfile.member_auth_id == user_id).first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "user": user}


@router.get("/auth/validate")
def validate_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    # Token validation logic here
    return {"message": "Token is valid"}


@router.post("/auth/register")
def register(
    register_request: RegisterMemberRequest,
    db: Session = Depends(get_db),
):
    tenant_object = (
        db.query(Tenant)
        .filter(Tenant.id == settings.default_tenant)
        .first()  # TODO: use register_request.tenant_id object to enable multi-tenancy
    )
    plan_object = (
        db.query(SubscriptionPlan)
        .filter(SubscriptionPlan.id == register_request.subscription_plan_id)
        .first()
    )
    if not plan_object:
        raise HTTPException(status_code=404, detail="Subscription plan not found")
    if not tenant_object:
        raise HTTPException(
            status_code=404,
            detail="Default tenant not found. Please contact support.",
        )

    existing_user = (
        db.query(MemberAuth).filter(MemberAuth.email == register_request.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail=f"Email already registered with {tenant_object.name}",
        )

    try:
        hashed_password = hash_password(register_request.password)
        new_user = MemberAuth(
            email=register_request.email,
            hashed_password=hashed_password,
            login_attempts=0,
            role=Role.MEMBER,
            state=MemberState.PENDING,
        )
        db.add(new_user)
        db.flush()  # Get the user ID before committing

        new_profile = MemberProfile(
            tenant_id=tenant_object.id,
            first_name=register_request.first_name,
            last_name=register_request.last_name,
            member_auth_id=new_user.id,
            birthday=register_request.date_of_birth,
            address=register_request.address,
            zip_code=register_request.zip_code,
            phone_number=register_request.phone,
            gender=register_request.gender,
        )
        db.add(new_profile)
        db.flush()  # Ensure user_id from MemberProfile is fetched before creating membership

        new_membership = Membership(
            member_id=new_profile.id,
            plan_id=plan_object.id,
            start_date=datetime.utcnow(),
            is_active=False,
        )
        db.add(new_membership)

        db.commit()
        db.refresh(new_user)
        db.refresh(new_membership)  # Ensure membership_id is available

        return {
            "message": "Registration successful",
            "user_id": new_user.id,
            "membership_id": new_membership.id,  # Include membership_id in response
        }

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred during registration"
        )


@router.put("/auth/change-password")
def change_password(
    request: ChangePasswordRequest,
    db: Session = Depends(get_db),
):
    user = db.query(MemberAuth).filter(MemberAuth.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(request.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    user.hashed_password = hash_password(request.new_password)
    db.add(user)
    db.commit()

    return {"message": "Password changed successfully"}
