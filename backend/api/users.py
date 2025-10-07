from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.models.user import (
    MemberAuth,
    MemberProfile,
)

router = APIRouter(prefix="/users")

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(MemberAuth).all()
    return {"status": "success", "users": users}


@router.get("/{user_id}")
def get_profile(user_id: int, db: Session = Depends(get_db)):
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
