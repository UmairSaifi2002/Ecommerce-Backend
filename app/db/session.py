from collections.abc import AsyncGenerator

from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config.settings import settings

# ----------------------------------------------------------
# Engine
# ----------------------------------------------------------
# Engine = connection pool + dialect. Ek process me ek hi engine.
# echo=True dev me SQL queries print karega, prod me off.
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
)


# ----------------------------------------------------------
# SQLite specific pragmas
# ----------------------------------------------------------
# SQLite me by default foreign keys OFF hote hain (surprise!).
# WAL mode = better concurrency (readers block writers nahi).
# hum ye pragmas har naye connection pe set karte hain.
@event.listens_for(engine.sync_engine, "connect")
def _set_sqlite_pragmas(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()


# ----------------------------------------------------------
# Session Factory
# ----------------------------------------------------------
# async_sessionmaker = factory that creates AsyncSession objects.
# expire_on_commit=False => after commit, loaded attributes still accessible.
# (Warna commit ke baad obj.attr access karne pe lazy load trigger hota,
#  async me ye silently fail karta hai.)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# ----------------------------------------------------------
# Dependency for FastAPI
# ----------------------------------------------------------
# async def get_db() -> AsyncGenerator[AsyncSession, None]:
async def get_db() -> AsyncGenerator[AsyncSession]:
    """
    Yields a database session per request.

    Pattern:
    - FastAPI dependency injection se har request ko naya session milta hai.
    - 'async with' ensures session properly closed after request.
    - On exception, rollback. On success, commit is caller's job.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
