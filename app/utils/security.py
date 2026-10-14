from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config.constants import UserRole
from app.config.settings import settings
from app.db.session import get_db
from app.middleware.error_handler import ForbiddenError, UnauthorizedError
from app.models.user import User
from app.managers.user_manager import UserManager

# ----------------------------------------------------------
# Password hashing
# ----------------------------------------------------------
# bcrypt: intentionally slow (work factor), salt built-in.
# Ye brute-force attacks ko expensive banata hai.
# MD5/SHA256 use KABHI nahi karte — wo fast hain, isliye insecure.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    """Plain password → bcrypt hash (salt + cost built-in)."""
    # bcrypt 72-byte limit hai; hum input truncate karte hain safely.
    return pwd_context.hash(plain[:72])


def verify_password(plain: str, hashed: str) -> bool:
    """Constant-time comparison (bcrypt internally)."""
    return pwd_context.verify(plain[:72], hashed)


# ----------------------------------------------------------
# JWT
# ----------------------------------------------------------
# Token kabhi password nahi rakhta. Sirf user_id (sub) + expiry.
# Signature verify hoti hai, encryption nahi hoti — JWT payload readable hai.
# Isliye secrets kabhi payload me na daalo.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def create_access_token(
    user_id: int,
    role: str,
    expires_minutes: int | None = None,
) -> str:
    """
    JWT create karo:
    - sub (subject) = user id as string (JWT spec)
    - role = quick role check client-side (optional)
    - exp = expiry timestamp (verification ke liye zaroori)
    - iat = issued-at time
    """
    expire_minutes = expires_minutes or settings.JWT_ACCESS_EXPIRE_MINUTES
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=expire_minutes),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """JWT verify karo, agar valid to payload return. Invalid par raise."""
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except JWTError as e:
        raise UnauthorizedError("Invalid or expired token") from e


# ----------------------------------------------------------
# Dependencies
# ----------------------------------------------------------
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """
    JWT se user resolve karo.
    - token decode
    - DB se user fetch
    - active check
    Return: User ORM object
    """
    payload = decode_token(token)
    user_id_raw = payload.get("sub")
    if user_id_raw is None:
        raise UnauthorizedError("Token missing subject")

    try:
        user_id = int(user_id_raw)
    except (TypeError, ValueError) as e:
        raise UnauthorizedError("Invalid token subject") from e

    user = await UserManager.get_by_id(db, user_id)

    if user is None:
        raise UnauthorizedError("User not found")
    if not user.is_active:
        raise ForbiddenError("User account is inactive")

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_role(*allowed_roles: UserRole):
    """
    Role guard factory.

    Usage:
        @router.get("/admin", dependencies=[Depends(require_role(UserRole.ADMIN))])
        @router.get("/seller-only")
        async def x(user: CurrentUser = Depends(require_role(UserRole.SELLER))):
            ...
    """
    async def _guard(user: CurrentUser) -> User:
        if user.role not in {r.value for r in allowed_roles}:
            raise ForbiddenError(
                f"Requires role: {', '.join(r.value for r in allowed_roles)}"
            )
        return user

    return _guard




