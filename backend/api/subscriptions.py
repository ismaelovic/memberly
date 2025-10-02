from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.db.session import get_db
from backend.models.subscriptions import SubscriptionPlan
from backend.schemas.subscriptions import SubscriptionCreate, SubscriptionUpdate

router = APIRouter()


@router.get("/subscriptions")
def get_subscriptions(db: Session = Depends(get_db)):
    # Filter out inactive subscriptions
    return db.query(SubscriptionPlan).filter(SubscriptionPlan.is_active == True).all()


@router.post("/subscriptions")
def create_subscription(
    subscription: SubscriptionCreate, db: Session = Depends(get_db)
):
    new_subscription = SubscriptionPlan(**subscription.dict())
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription


@router.put("/subscriptions/{subscription_id}")
def update_subscription(
    subscription_id: int,
    subscription: SubscriptionUpdate,
    db: Session = Depends(get_db),
):
    existing_subscription = (
        db.query(SubscriptionPlan)
        .filter(SubscriptionPlan.id == subscription_id)
        .first()
    )
    if not existing_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    for key, value in subscription.dict().items():
        setattr(existing_subscription, key, value)

    db.commit()
    db.refresh(existing_subscription)
    return existing_subscription


@router.delete("/subscriptions/{subscription_id}")
def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    existing_subscription = (
        db.query(SubscriptionPlan)
        .filter(SubscriptionPlan.id == subscription_id)
        .first()
    )
    if not existing_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    db.delete(existing_subscription)
    db.commit()
    return {"message": "Subscription deleted successfully"}
