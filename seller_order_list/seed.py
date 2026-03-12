import uuid
import asyncio

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import engine, AsyncSessionLocal
from app.database.base import Base

from app.models.user import User
from app.models.market import Market
from app.models.product import Product
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem

from app.enums.product_category import ProductCategory


async def seed():

    print("Creating tables if not exist...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:

        print("Cleaning database...")

        await db.execute(delete(OrderItem))
        await db.execute(delete(Order))
        await db.execute(delete(Product))
        await db.execute(delete(Market))
        await db.execute(delete(User))

        await db.commit()

        print("Creating users...")

        seller_id = uuid.UUID("9ba4ee01-186e-48a8-a638-a6804d4def84")
        buyer_id = uuid.uuid4()

        seller = User(
            userId=seller_id,
            login="seller",
            passwordHash="123",
            firstName="Ivan",
            lastName="Petrov",
            patronymic="Ivanovich",
            city="Amsterdam",
            telegram="@seller_test",
            telegramChatId="12345678",
            isSeller=True
        )

        buyer = User(
            userId=buyer_id,
            login="buyer",
            passwordHash="123",
            firstName="Anna",
            lastName="Ivanova",
            patronymic="Sergeevna",
            city="Amsterdam",
            telegram="@buyer_test",
            telegramChatId="87654321",
            isSeller=False
        )

        db.add_all([seller, buyer])
        await db.commit()

        print("Creating market...")

        market = Market(
            userId=seller_id,
            marketName="Electronics Store",
            description="Test electronics marketplace"
        )

        db.add(market)
        await db.commit()
        await db.refresh(market)

        print("Creating products...")

        iphone = Product(
            marketId=market.marketId,
            name="iPhone 15",
            description="Apple smartphone",
            category=ProductCategory.electronics,
            price=1200,
            available=100,
            img="iphone.jpg"
        )

        tv = Product(
            marketId=market.marketId,
            name="Samsung TV",
            description="Smart TV 55 inch",
            category=ProductCategory.electronics,
            price=900,
            available=40,
            img="tv.jpg"
        )

        book = Product(
            marketId=market.marketId,
            name="Python Book",
            description="Learn Python",
            category=ProductCategory.books,
            price=50,
            available=200,
            img="python.jpg"
        )

        db.add_all([iphone, tv, book])
        await db.commit()

        await db.refresh(iphone)
        await db.refresh(tv)
        await db.refresh(book)

        print("Creating orders...")

        order1 = Order(
            marketId=market.marketId,
            userId=buyer_id,
            orderNumber="ORD-1001",
            deliveryAddress="Amsterdam, Main Street 10",
            totalAmount=2100,
            status=OrderStatus.processing
        )

        order2 = Order(
            marketId=market.marketId,
            userId=buyer_id,
            orderNumber="ORD-1002",
            deliveryAddress="Amsterdam, River Street 5",
            totalAmount=900,
            status=OrderStatus.pending
        )

        order3 = Order(
            marketId=market.marketId,
            userId=buyer_id,
            orderNumber="ORD-1003",
            deliveryAddress="Amsterdam, Flower Street 7",
            totalAmount=50,
            status=OrderStatus.completed
        )

        db.add_all([order1, order2, order3])
        await db.commit()

        await db.refresh(order1)
        await db.refresh(order2)
        await db.refresh(order3)

        print("Creating order items...")

        items = [

            OrderItem(
                orderId=order1.id,
                productId=iphone.id,
                quantity=1,
                price=1200
            ),

            OrderItem(
                orderId=order1.id,
                productId=tv.id,
                quantity=1,
                price=900
            ),

            OrderItem(
                orderId=order2.id,
                productId=tv.id,
                quantity=1,
                price=900
            ),

            OrderItem(
                orderId=order3.id,
                productId=book.id,
                quantity=1,
                price=50
            ),
        ]

        db.add_all(items)
        await db.commit()

        print("Seed completed successfully")

        print()
        print("SELLER JWT TOKEN:")
        print("--------------------------------------------------")

        print(
            "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJ1c2VySWQiOiI5YmE0ZWUwMS0xODZlLTQ4YTgtYTYzOC1hNjgwNGQ0ZGVmODQiLCJpc1NlbGxlciI6dHJ1ZX0."
            "aZRdraajXo4TDSsX_wQlu7XMeBGA081R7RfjZUzDf8U"
        )

        print("--------------------------------------------------")


if __name__ == "__main__":
    asyncio.run(seed())