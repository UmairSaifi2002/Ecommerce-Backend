from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User


class UserManager:

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
        """User with profiles preloaded (avoid lazy-load async error)."""
        result = await db.execute(
            select(User)
            .options(
                selectinload(User.buyer_profile),
                selectinload(User.seller_profile),
            )
            .where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    def _with_profiles(stmt):
        """
        Eager load buyer_profile + seller_profile.
        Har query me manually likhne se better — ek jagah maintain.
        """
        return stmt.options(
            selectinload(User.buyer_profile),
            selectinload(User.seller_profile),
        )

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        stmt = UserManager._with_profiles(select(User)).where(User.email == email)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    



