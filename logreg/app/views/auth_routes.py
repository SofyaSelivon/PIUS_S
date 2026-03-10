from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse
from app.controllers.auth_controller import register_user, login_user
from app.models.user_token import UserToken
from typing import Optional
from uuid import UUID

router = APIRouter(prefix="/api/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=AuthResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    user, result = register_user(db, request)

    if not user:
        return {"success": False, "message": result}

    return {
        "success": True,
        "user": {
            "userId": user.userId,
            "login": user.login,
            "firstName": user.firstName,
            "isSeller": user.isSeller
        },
        "token": result
    }


@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user, result = login_user(db, request)

    if not user:
        return {"success": False, "message": result}

    return {
        "success": True,
        "user": {
            "userId": user.userId,
            "login": user.login,
            "firstName": user.firstName,
            "isSeller": user.isSeller
        },
        "token": result
    }
@router.get("/token/{user_id}", response_model=Optional[str])
def get_user_token(user_id: UUID, db: Session = Depends(get_db)):
    token_record = (
        db.query(UserToken)
        .filter(UserToken.userId == user_id)
        .order_by(UserToken.expiresAt.desc())
        .first()
    )

    if not token_record:
        raise HTTPException(status_code=404, detail="Token not found")

    from datetime import datetime
    if token_record.expiresAt < datetime.utcnow():
        raise HTTPException(status_code=403, detail="Token expired")

    return token_record.token