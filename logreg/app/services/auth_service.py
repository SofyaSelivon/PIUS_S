from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.market import Market
from app.models.user_token import UserToken
from app.core.security import hash_password, verify_password, create_access_token
from datetime import datetime, timedelta
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

class AuthService:

    @staticmethod
    def register(db: Session, request):

        existing_user = UserRepository.get_by_login(db, request.login)
        if existing_user:
            return None, "Login already exists"

        user = User(
            login=request.login,
            passwordHash=hash_password(request.password),
            firstName=request.firstName,
            lastName=request.lastName,
            patronymic=request.patronymic,
            dateOfBirth=request.dateOfBirth,
            city=request.city,
            telegram=request.telegram,
            isSeller=request.isSeller
        )
        user = UserRepository.create_user(db, user)

        if request.isSeller:
            market = Market(
                userId=user.userId,
                marketName=f"{user.firstName}'s Market"
            )
            UserRepository.create_market(db, market)

        token_str = create_access_token({"sub": str(user.userId)})
        token = UserToken(
            userId=user.userId,
            token=token_str,
            expiresAt=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        db.add(token)
        db.commit()
        db.refresh(token)

        return user, token_str

    @staticmethod
    def login(db: Session, request):

        user = UserRepository.get_by_login(db, request.login)
        if not user:
            return None, "Invalid login or password"

        if not verify_password(request.password, user.passwordHash):
            return None, "Invalid login or password"

        token_str = create_access_token({"sub": str(user.userId)})
        token = UserToken(
            userId=user.userId,
            token=token_str,
            expiresAt=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        db.add(token)
        db.commit()
        db.refresh(token)

        return user, token_str