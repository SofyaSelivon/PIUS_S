import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.models.user import User
from app.models.market import Market
from app.models.user_token import UserToken
from app.core.security import hash_password, create_access_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES


TEST_LOGIN = f"testuser_{uuid.uuid4().hex[:6]}"
TEST_PASSWORD = "password123"
FIRST_NAME = "Test"
LAST_NAME = "User"
CITY = "TestCity"
DATE_OF_BIRTH = datetime(1990, 1, 1).date()


def seed():
    db: Session = SessionLocal()
    try:
        # создаём пользователя
        user = User(
            login=TEST_LOGIN,
            passwordHash=hash_password(TEST_PASSWORD),
            firstName=FIRST_NAME,
            lastName=LAST_NAME,
            dateOfBirth=DATE_OF_BIRTH,
            city=CITY,
            isSeller=True  # для примера создаём продавца
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # создаём маркет, если продавец
        market = Market(
            userId=user.userId,
            marketName=f"{user.firstName}'s Market",
            description="Test market"
        )
        db.add(market)
        db.commit()
        db.refresh(market)

        # создаём токен
        token_str = create_access_token({"sub": str(user.userId)})
        token = UserToken(
            userId=user.userId,
            token=token_str,
            expiresAt=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        db.add(token)
        db.commit()
        db.refresh(token)

        # выводим для проверки
        print("Test user created!")
        print(f"Login: {TEST_LOGIN}")
        print(f"Password: {TEST_PASSWORD}")
        print(f"userId: {user.userId}")
        print(f"Token: {token.token}")

    finally:
        db.close()


if __name__ == "__main__":
    seed()