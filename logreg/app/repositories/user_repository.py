from sqlalchemy.orm import Session
from app.models.user import User
from app.models.market import Market


class UserRepository:

    @staticmethod
    def get_by_login(db: Session, login: str):
        return db.query(User).filter(User.login == login).first()

    @staticmethod
    def create_user(db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def create_market(db: Session, market: Market):
        db.add(market)
        db.commit()
        db.refresh(market)
        return market