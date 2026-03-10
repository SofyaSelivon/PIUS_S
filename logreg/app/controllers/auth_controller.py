from sqlalchemy.orm import Session
from app.services.auth_service import AuthService


def register_user(db: Session, request):
    return AuthService.register(db, request)


def login_user(db: Session, request):
    return AuthService.login(db, request)