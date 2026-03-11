from sqlalchemy.orm import Session
from app.models.market import Market
from app.models.product import Product
from fastapi import HTTPException


# ======================================================
# 3️⃣ GET /api/products/my
# ======================================================
def get_my_products(
        db: Session,
        user_id,
        page,
        limit,
        search,
        category,
        min_price,
        max_price,
        available
):
    market = db.query(Market).filter(Market.userId == user_id).first()
    if not market:
        return {"items": [], "pagination": {}}

    query = db.query(Product).filter(Product.marketId == market.marketId)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if category:
        query = query.filter(Product.category == category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if available is not None and available:
        query = query.filter(Product.available > 0)

    total_items = query.count()
    offset = (page - 1) * limit
    products = query.offset(offset).limit(limit).all()
    total_pages = (total_items + limit - 1) // limit

    return {
        "items": products,
        "pagination": {
            "page": page,
            "limit": limit,
            "totalItems": total_items,
            "totalPages": total_pages
        }
    }


# ======================================================
# 4️⃣ POST /api/products
# ======================================================
def create_product(db: Session, user_id, data):
    market = db.query(Market).filter(Market.userId == user_id).first()
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")

    product = Product(
        marketId=market.marketId,
        name=data.name,
        description=data.description,
        category=data.category,
        price=data.price,
        available=data.available,
        img=data.img
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


# ======================================================
# 5️⃣ GET /api/products/:id
# ======================================================
def get_product(db: Session, product_id, user_id):
    market = db.query(Market).filter(Market.userId == user_id).first()
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")

    product = db.query(Product).filter(
        Product.id == product_id,
        Product.marketId == market.marketId
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# ======================================================
# 6️⃣ PATCH /api/products/:id
# ======================================================
def update_product(db: Session, product_id, user_id, data):
    product = get_product(db, product_id, user_id)

    if data.name is not None:
        product.name = data.name
    if data.price is not None:
        product.price = data.price
    if data.available is not None:
        product.available = data.available

    db.commit()
    db.refresh(product)

    return product