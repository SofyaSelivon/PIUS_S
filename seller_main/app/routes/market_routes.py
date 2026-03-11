from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.controllers.market_controller import get_my_market, update_market
from app.schemas.market_schema import MarketUpdate
from app.security.jwt_dependency import get_current_user

router = APIRouter(prefix="/api/markets", tags=["markets"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/my")
def my_market(
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    market = get_my_market(db, user["userId"])
    if not market:
        return {"market": None}
    return market


@router.patch("/my")
def update_my_market(
        data: MarketUpdate,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    update_market(db, user["userId"], data)
    return {"success": True}