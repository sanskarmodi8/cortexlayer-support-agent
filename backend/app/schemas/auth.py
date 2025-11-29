"""Schemas for authentication requests and responses."""

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Schema for login request."""

    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    """Schema for registration request."""

    email: EmailStr
    password: str
    company_name: str


class TokenResponse(BaseModel):
    """Response schema for successful auth."""

    access_token: str
    token_type: str = "bearer"
