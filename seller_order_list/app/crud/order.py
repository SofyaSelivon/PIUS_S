from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.user import User


def get_orders_with_stats(db: Session, market_id, status=None, page: int = 1, limit: int = 10):

    query = (
        db.query(
            Order,
            func.count(OrderItem.id).label("itemsCount"),
            User.userId,
            User.firstName,
            User.lastName,
            User.patronymic,
            User.telegram
        )
        .join(User, User.userId == Order.userId)
        .outerjoin(OrderItem, OrderItem.orderId == Order.id)
        .filter(Order.marketId == market_id, Order.deletedAt.is_(None))
        .group_by(Order.id, User.userId)
    )

    if status:
        query = query.filter(Order.status == status)

    total_orders = db.query(func.count(Order.id)).filter(
        Order.marketId == market_id,
        Order.deletedAt.is_(None)
    ).scalar()

    total_revenue = db.query(
        func.coalesce(func.sum(Order.totalAmount), 0)
    ).filter(
        Order.marketId == market_id,
        Order.status != OrderStatus.cancelled,
        Order.deletedAt.is_(None)
    ).scalar()

    completed_orders = db.query(func.count(Order.id)).filter(
        Order.marketId == market_id,
        Order.status == OrderStatus.completed,
        Order.deletedAt.is_(None)
    ).scalar()

    processing_orders = db.query(func.count(Order.id)).filter(
        Order.marketId == market_id,
        Order.status.in_([OrderStatus.processing, OrderStatus.shipped]),
        Order.deletedAt.is_(None)
    ).scalar()

    pending_orders = db.query(func.count(Order.id)).filter(
        Order.marketId == market_id,
        Order.status == OrderStatus.pending,
        Order.deletedAt.is_(None)
    ).scalar()

    rows = query.offset((page - 1) * limit).limit(limit).all()

    orders = []

    for order, items_count, uid, first, last, pat, telegram in rows:

        full_name = " ".join(filter(None, [first, last, pat]))

        orders.append({
            "id": order.id,
            "orderNumber": order.orderNumber,
            "customer": {
                "id": uid,
                "fullName": full_name,
                "telegram": telegram
            },
            "deliveryAddress": order.deliveryAddress,
            "totalAmount": float(order.totalAmount),
            "itemsCount": items_count,
            "status": order.status,
            "createdAt": order.createdAt
        })

    return {
        "statistics": {
            "totalOrders": total_orders,
            "totalRevenue": float(total_revenue),
            "completedOrders": completed_orders,
            "processingOrders": processing_orders,
            "pendingOrders": pending_orders
        },
        "orders": orders,
        "pagination": {
            "page": page,
            "limit": limit,
            "totalItems": total_orders,
            "totalPages": (total_orders + limit - 1) // limit
        }
    }


def update_order_status(db: Session, order: Order, new_status: OrderStatus):
    order.status = new_status
    db.commit()
    return True


def soft_delete_order(db: Session, order: Order):
    order.deletedAt = func.now()
    db.commit()
    return True