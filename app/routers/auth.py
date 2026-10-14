from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.db.session import get_db
from app.managers.auth_manager import AuthManager
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    TokenResponse,
)
from app.schemas.user import UserResponse
from app.utils.security import CurrentUser, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserResponse:
    """
    Register a new buyer or seller.
    Returns the created user (no password).
    """
    user = await AuthManager.register(db, payload)
    return UserResponse.model_validate(user)


@router.post("/login", response_model=LoginResponse)
async def login(
    payload: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LoginResponse:
    """
    Login with email + password.
    Returns JWT access token + user info.
    """
    user = await AuthManager.authenticate(db, payload.email, payload.password)
    token = create_access_token(user_id=user.id, role=user.role)
    return LoginResponse(
        access_token=token,
        expires_in=settings.JWT_ACCESS_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
async def me(current_user: CurrentUser) -> UserResponse:
    """Return the currently authenticated user."""
    return UserResponse.model_validate(current_user)







