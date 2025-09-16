from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.schemas.membership import (
    MembershipCreate,
    MembershipUpdate,
    MembershipResponse,
)
from backend.models.membership import Membership
from typing import List

router = APIRouter()


@router.post("/memberships", response_model=MembershipResponse)
def create_membership(membership: MembershipCreate, db: Session = Depends(get_db)):
    new_membership = Membership(**membership.dict())
    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)
    return new_membership


@router.get("/memberships", response_model=List[MembershipResponse])
def list_memberships(db: Session = Depends(get_db)):
    return db.query(Membership).all()


@router.get("/memberships/{membership_id}", response_model=MembershipResponse)
def get_membership(membership_id: int, db: Session = Depends(get_db)):
    db_membership = db.query(Membership).filter(Membership.id == membership_id).first()
    if not db_membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    return db_membership


@router.put("/memberships/{membership_id}", response_model=MembershipResponse)
def update_membership(
    membership_id: int, membership: MembershipUpdate, db: Session = Depends(get_db)
):
    db_membership = db.query(Membership).filter(Membership.id == membership_id).first()
    if not db_membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    for key, value in membership.dict(exclude_unset=True).items():
        setattr(db_membership, key, value)
    db.commit()
    db.refresh(db_membership)
    return db_membership


@router.delete("/memberships/{membership_id}")
def delete_membership(membership_id: int, db: Session = Depends(get_db)):
    db_membership = db.query(Membership).filter(Membership.id == membership_id).first()
    if not db_membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    db.delete(db_membership)
    db.commit()
    return {"detail": "Membership deleted successfully"}
