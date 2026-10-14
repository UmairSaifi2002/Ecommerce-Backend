from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict:
    """Liveness probe — app zinda hai?"""
    return {"status": "ok"}


@router.get("/ready")
async def ready(db: AsyncSession = Depends(get_db)) -> dict:
    """
    Readiness probe — app dependencies (DB, Redis) ready hain?
    Kubernetes/load balancer isko use karte hain.
    """
    await db.execute(text("SELECT 1"))
    return {"status": "ready", "db": "ok"}
