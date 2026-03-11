from sqlalchemy.orm import Session
from app.models.market import Market
from fastapi import HTTPException


def get_my_market(db: Session, user_id):
    market = db.query(Market).filter(Market.userId == user_id).first()
    return market


def update_market(db: Session, user_id, data):
    market = db.query(Market).filter(Market.userId == user_id).first()

    if not market:
        raise HTTPException(status_code=404, detail="Market not found")

    market.marketName = data.marketName
    market.description = data.description

    db.commit()
    db.refresh(market)

    return market