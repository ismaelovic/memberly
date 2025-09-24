from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.schemas.member import MemberCreate, MemberUpdate, MemberResponse
from backend.models.user import MemberAuth, MemberProfile
from typing import List

router = APIRouter()


@router.post("/members", response_model=MemberResponse)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    db_member = db.query(MemberAuth).filter(MemberAuth.email == member.email).first()
    if db_member:
        raise HTTPException(
            status_code=400, detail="Member with this email already exists"
        )
    new_member = MemberAuth(**member.dict())
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


@router.get("/members", response_model=List[MemberResponse])
def list_members(db: Session = Depends(get_db)):
    return db.query(MemberProfile).all()


@router.get("/members/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(MemberProfile).filter(MemberProfile.id == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


@router.put("/members/{member_id}", response_model=MemberResponse)
def update_member(member_id: int, member: MemberUpdate, db: Session = Depends(get_db)):
    db_member = db.query(MemberProfile).filter(MemberProfile.id == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    for key, value in member.dict(exclude_unset=True).items():
        setattr(db_member, key, value)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.delete("/members/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(MemberProfile).filter(MemberProfile.id == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(db_member)
    db.commit()
    return {"detail": "Member deleted successfully"}
