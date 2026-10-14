from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload 

from app.config.constants import BuyerTier, UserRole
from app.middleware.error_handler import ConflictError, UnauthorizedError
from app.models.user import BuyerProfile, SellerProfile, User
from app.schemas.auth import RegisterRequest
from app.utils.security import hash_password, verify_password
from app.managers.user_manager import UserManager

class AuthManager:
    """
    Auth-related business logic.

    Manager responsibilities:
    - DB writes/reads for auth flows
    - Raise domain exceptions (AppError subclasses)
    - NEVER touch HTTP (no status codes, no requests)
    """

    @staticmethod
    async def register(db: AsyncSession, payload: RegisterRequest) -> User:
        """
        Register a buyer or seller.
        - email unique check
        - password hash
        - role-specific profile create
        - transaction commit
        """
        # 1. Duplicate email check (fast-fail, DB constraint bhi hai)
        existing = await db.execute(select(User.id).where(User.email == payload.email))
        if existing.scalar_one_or_none() is not None:
            raise ConflictError("Email already registered")

        # 2. Create user
        user = User(
            email=payload.email,
            hashed_password=hash_password(payload.password),
            full_name=payload.full_name,
            role=payload.role,
        )
        db.add(user)
        await db.flush()  # get user.id without committing

        # 3. Role-specific profile
        if payload.role == UserRole.BUYER.value:
            db.add(BuyerProfile(user_id=user.id, current_tier=BuyerTier.BASIC.value))
        elif payload.role == UserRole.SELLER.value:
            if not payload.store_name:
                raise ConflictError("store_name required for seller")
            db.add(SellerProfile(user_id=user.id, store_name=payload.store_name))

        # 4. Commit (caller session handle karega, but manager commits for clarity)
        try:
            await db.commit()
        except IntegrityError as e:
            await db.rollback()
            raise ConflictError("Email already registered") from e

        # await db.refresh(user)
        # ✅ Eager-loaded user return
        user = await UserManager.get_by_id(db, user.id)
        assert user is not None   # we just created it
        return user

    @staticmethod
    async def authenticate(db: AsyncSession, email: str, password: str) -> User:
        """
        Login flow.
        - Email se user dhoondo
        - Password verify (constant-time)
        - Inactive check
        """
        # result = await db.execute(select(User).where(User.email == email))
        result = await db.execute(
            select(User)
            .options(
                selectinload(User.buyer_profile),
                selectinload(User.seller_profile),
            )
            .where(User.email == email)
        )
        user = result.scalar_one_or_none()

        # Timing-safe: user not found pe bhi verify call karo (dummy hash)
        if user is None or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")

        if not user.is_active:
            raise UnauthorizedError("Account is inactive")

        return user

    

    