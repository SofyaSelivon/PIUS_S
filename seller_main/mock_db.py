import uuid
import asyncio
from decimal import Decimal
from jose import jwt
from sqlalchemy import delete
from app.database.session import AsyncSessionLocal
from app.models.user import User
from app.models.market import Market
from app.models.product import Product
from app.enums.product_category import ProductCategory

SECRET_KEY = "secret"
ALGORITHM = "HS256"

async def seed():
    async with AsyncSessionLocal() as db:
        print("Cleaning tables...")

        # Сначала продукты, потом маркет, потом юзеры — чтобы FK не ломались
        await db.execute(delete(Product))
        await db.execute(delete(Market))
        await db.execute(delete(User))
        await db.commit()

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
        await db.commit()
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
        await db.commit()
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
        await db.commit()
        print("Products created:", len(products))

        # ======================================================
        # JWT
        # ======================================================
        payload = {
            "userId": str(seller_id),
            "isSeller": True
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        print("\nJWT token for Swagger / curl:")
        print(token)
        print(str(seller_id))


if __name__ == "__main__":
    asyncio.run(seed())