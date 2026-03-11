from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.crud import order as crud_order
from app.schemas.order import PaginatedOrdersOut, OrderStatusUpdate, SuccessResponse
from app.deps import get_current_user

from app.models.order import Order
from app.models.market import Market


router = APIRouter(prefix="/api/seller/orders", tags=["seller"])


@router.get("", response_model=PaginatedOrdersOut)
def list_orders(
        page: int = Query(1),
        limit: int = Query(10),
        status: str | None = Query(None),
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):

    market_id = db.query(Market.marketId).filter(
        Market.userId == current_user["userId"]
    ).scalar()

    if not market_id:
        return {"statistics": {}, "orders": [], "pagination": {}}

    return crud_order.get_orders_with_stats(db, market_id, status, page, limit)


@router.patch("/{order_id}/status", response_model=SuccessResponse)
def update_status(
        order_id: str = Path(...),
        status_update: OrderStatusUpdate = None,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):

    market_id = db.query(Market.marketId).filter(
        Market.userId == current_user["userId"]
    ).scalar()

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.marketId == market_id,
        Order.deletedAt.is_(None)
    ).first()

    if not order:
        raise HTTPException(404, "Order not found")

    crud_order.update_order_status(db, order, status_update.status)

    return {"success": True}


@router.delete("/{order_id}", response_model=SuccessResponse)
def delete_order(
        order_id: str = Path(...),
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):

    market_id = db.query(Market.marketId).filter(
        Market.userId == current_user["userId"]
    ).scalar()

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.marketId == market_id,
        Order.deletedAt.is_(None)
    ).first()

    if not order:
        raise HTTPException(404, "Order not found")

    crud_order.soft_delete_order(db, order)

    return {"success": True}