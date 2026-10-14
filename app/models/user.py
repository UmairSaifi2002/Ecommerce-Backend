from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.constants import BuyerTier, UserRole
from app.db.base import Base


class User(Base):
    """
    Core user table — sab buyers, sellers, admins yahin hain.

    Role-based design:
    - role column determines what the user can do
    - Profile-specific data (buyer_tier, store_name) separate tables me
    - Isse schema clean rehta hai, aur future me naye roles add karna easy
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    role: Mapped[str] = mapped_column(
        String(20), nullable=False, default=UserRole.BUYER.value
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships (one-to-one)
    buyer_profile: Mapped["BuyerProfile | None"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
    seller_profile: Mapped["SellerProfile | None"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} role={self.role}>"


class BuyerProfile(Base):
    """
    Buyer-specific data. Ek user buyer hai to uska ek BuyerProfile hoga.
    Basic/Ultra/Pro tier yahan track hota hai.
    """

    __tablename__ = "buyer_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False,
    )
    current_tier: Mapped[str] = mapped_column(
        String(20), nullable=False, default=BuyerTier.BASIC.value
    )
    stripe_customer_id: Mapped[str | None] = mapped_column(
        String(120), unique=True, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationship back to user
    user: Mapped["User"] = relationship(back_populates="buyer_profile")


class SellerProfile(Base):
    """
    Seller-specific data. Store info, Stripe Connect account, payout balance.
    """

    __tablename__ = "seller_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False,
    )
    store_name: Mapped[str] = mapped_column(String(120), nullable=False)
    stripe_account_id: Mapped[str | None] = mapped_column(
        String(120), unique=True, nullable=True
    )
    kyc_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="seller_profile")



    