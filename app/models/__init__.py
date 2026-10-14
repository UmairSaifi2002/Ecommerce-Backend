"""
Models package.

IMPORTANT: Saare models yahan import karo.
Isse do fayde:
1. `from app import models` karne se saare tables Base.metadata me register ho jaate hain
2. Alembic migrations autogenerate me saare tables detect hote hain
3. __all__ se explicit public API
"""

from app.models.user import BuyerProfile, SellerProfile, User

__all__ = ["User", "BuyerProfile", "SellerProfile"]




