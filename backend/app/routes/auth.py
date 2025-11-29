"""Routes for authentication (register + login)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.auth import (
    create_access_token,
    hash_password,
    verify_password,
)
from backend.app.core.database import get_db
from backend.app.models.client import Client
from backend.app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse)
async def register_user(
    request: RegisterRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Register a new client and return a JWT token."""
    existing = db.query(Client).filter(Client.email == request.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    client = Client(
        email=request.email,
        hashed_password=hash_password(request.password),
        company_name=request.company_name,
    )
    db.add(client)
    db.commit()
    db.refresh(client)

    token = create_access_token({"sub": str(client.id)})
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
async def login_user(
    request: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Login existing client and return access token."""
    client = db.query(Client).filter(Client.email == request.email).first()

    if not client or not verify_password(request.password, client.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if client.is_disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account disabled",
        )

    token = create_access_token({"sub": str(client.id)})
    return TokenResponse(access_token=token)
