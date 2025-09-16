from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.schemas.communication import CommunicationCreate, CommunicationResponse
from backend.models.communication import Communication
from typing import List

router = APIRouter()


@router.post("/communications", response_model=CommunicationResponse)
def send_communication(
    communication: CommunicationCreate, db: Session = Depends(get_db)
):
    new_communication = Communication(**communication.dict())
    db.add(new_communication)
    db.commit()
    db.refresh(new_communication)
    return new_communication


@router.get("/communications", response_model=List[CommunicationResponse])
def list_communications(db: Session = Depends(get_db)):
    return db.query(Communication).all()
