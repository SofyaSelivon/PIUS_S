from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.controllers.product_controller import *
from app.schemas.product_schema import *
from app.security.jwt_dependency import get_current_user

router = APIRouter(prefix="/api/products", tags=["products"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/my")
def my_products(
        page: int = 1,
        limit: int = 12,
        search: str | None = None,
        category: ProductCategory | None = None,
        minPrice: float | None = None,
        maxPrice: float | None = None,
        available: bool | None = None,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    return get_my_products(
        db=db,
        user_id=user["userId"],
        page=page,
        limit=limit,
        search=search,
        category=category,
        min_price=minPrice,
        max_price=maxPrice,
        available=available
    )


@router.post("/")
def create(
        data: ProductCreate,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    product = create_product(db, user["userId"], data)
    return {"success": True, "productId": product.id}


@router.get("/{product_id}")
def get_product_by_id(
        product_id: str,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    product = get_product(db, product_id, user["userId"])
    return product


@router.patch("/{product_id}")
def update_product_by_id(
        product_id: str,
        data: ProductUpdate,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    update_product(db, product_id, user["userId"], data)
    return {"success": True}