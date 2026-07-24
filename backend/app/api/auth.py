"""
Auth API router.
Handles POST /login, POST /logout, GET /me.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, UserOut
from app.services.auth_service import (
    verify_password,
    create_token,
    get_current_user,
)

logger = logging.getLogger("eventflow.auth")

router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate and return a JWT token."""
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    token = create_token(user.id, user.email, user.role)

    logger.info("Login: %s (%s)", user.email, user.role)

    return LoginResponse(
        success=True,
        token=token,
        user={"name": user.name, "role": user.role},
    )


@router.post("/logout")
def logout():
    """
    Logout — client should discard the token.
    Server-side JWT is stateless, so nothing to invalidate.
    """
    return {"success": True, "message": "Logged out."}


@router.get("/me", response_model=UserOut)
def get_me(user: User = Depends(get_current_user)):
    """Return the current authenticated user's info."""
    return UserOut(name=user.name, email=user.email, role=user.role)
