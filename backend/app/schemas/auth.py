"""
Pydantic schemas for authentication.
"""

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Request body for POST /login."""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Response body after successful login."""
    success: bool
    token: str
    user: dict  # { name, role }


class UserOut(BaseModel):
    """Response body for GET /me."""
    name: str
    email: str
    role: str
