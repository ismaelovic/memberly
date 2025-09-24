from fastapi import APIRouter, Response, Request, HTTPException, Depends
from datetime import timedelta, datetime
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from backend.db.session import get_db
from backend.models.user import MemberAuth, MemberProfile
from backend.models.membership import Membership
from backend.core.security import create_access_token, verify_password, hash_password

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class LoginRequest(BaseModel):
    email: str
    password: str


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
    return {"message": "Login successful"}


@router.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logout successful"}


@router.get("/auth/validate")
def validate_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    # Token validation logic here
    return {"message": "Token is valid"}


class RegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    address: str
    phone: str
    subscription_plan_id: int


@router.post("/auth/register")
def register(
    register_request: RegisterRequest,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(MemberAuth).filter(MemberAuth.email == register_request.email).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    try:
        hashed_password = hash_password(register_request.password)
        new_user = MemberAuth(
            email=register_request.email, hashed_password=hashed_password
        )
        db.add(new_user)
        db.flush()  # Get the user ID before committing

        new_profile = MemberProfile(
            user_id=new_user.id,
            first_name=register_request.first_name,
            last_name=register_request.last_name,
            address=register_request.address,
            phone=register_request.phone,
        )
        db.add(new_profile)

        new_membership = Membership(
            user_id=new_user.id,
            subscription_plan_id=register_request.subscription_plan_id,
            start_date=datetime.utcnow(),
        )
        db.add(new_membership)

        db.commit()
        db.refresh(new_user)

        return {"message": "Registration successful", "user_id": new_user.id}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="An error occurred during registration"
        )
