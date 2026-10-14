import logging

from app.db.base import Base
from app.db.session import engine
# app/db/__init__.py
# from app.db.init_db import init_db

# __all__ = ["init_db"]

# IMPORTANT: importing models package registers all models with Base.metadata.
# Without this import, Base.metadata.create_all will create ZERO tables.
from app import models  # noqa: F401

logger = logging.getLogger(__name__)


async def init_db() -> None:
    """
    Dev-time helper: create all tables from models.

    In production we use Alembic migrations.
    For dev with SQLite, create_all is fast and convenient.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created (if not exist)")
