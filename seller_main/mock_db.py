import uuid
from decimal import Decimal

from app.database.session import SessionLocal
from app.models.user import User
from app.models.market import Market
from app.models.product import Product
from app.enums.product_category import ProductCategory

db = SessionLocal()

print("Cleaning tables...")

db.query(Product).delete()
db.query(Market).delete()
db.query(User).delete()

db.commit()

# ======================================================
# USER
# ======================================================

seller_id = uuid.uuid4()

seller = User(
    userId=seller_id,
    login="seller_test",
    passwordHash="hashed_password",
    firstName="Ivan",
    lastName="Petrov",
    city="Moscow",
    isSeller=True
)

db.add(seller)

# ⚠️ ВАЖНО
db.commit()

print("User created:", seller_id)

# ======================================================
# MARKET
# ======================================================

market_id = uuid.uuid4()

market = Market(
    marketId=market_id,
    userId=seller_id,
    marketName="Tech Store",
    description="Electronics and gadgets"
)

db.add(market)

# ⚠️ снова сохраняем
db.commit()

print("Market created:", market_id)

# ======================================================
# PRODUCTS
# ======================================================

products = [

    Product(
        marketId=market_id,
        name="iPhone 15",
        description="Apple smartphone",
        category=ProductCategory.electronics,
        price=Decimal("999.99"),
        available=10,
        img="https://example.com/iphone.jpg"
    ),

    Product(
        marketId=market_id,
        name="MacBook Pro",
        description="Apple laptop",
        category=ProductCategory.electronics,
        price=Decimal("2499.99"),
        available=5,
        img="https://example.com/macbook.jpg"
    ),

    Product(
        marketId=market_id,
        name="Gaming Mouse",
        description="RGB gaming mouse",
        category=ProductCategory.electronics,
        price=Decimal("79.99"),
        available=25,
        img="https://example.com/mouse.jpg"
    )
]

db.add_all(products)

db.flush()

print("Products created:", len(products))

print("\nDONE")
print("seller userId:", seller_id)

db.close()