from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.models.tenant import OnboardingToken


def validate_token(db: Session, token: str):
    invite = db.query(OnboardingToken).filter(OnboardingToken.token == token).first()
    if not invite:
        raise HTTPException(status_code=400, detail="Invalid token")
    if invite.used is True:
        raise HTTPException(status_code=400, detail="Token already used")
    if invite.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")
    return True
