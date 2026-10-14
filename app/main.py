import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.settings import settings
from app.db import init_db
from app.middleware.error_handler import (
    add_request_id_middleware,
    register_exception_handlers,
)
from app.routers import health
from app.utils.logging import setup_logging
from app.routers import auth, buyers, health, sellers 

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager (FastAPI 2.0+ way).

    Replaces @app.on_event("startup") / ("shutdown").
    Code before yield = startup. Code after yield = shutdown.
    """
    setup_logging()
    logger.info("Starting app | env=%s", settings.ENV)

    if settings.is_dev:
        await init_db()
        logger.info("Dev mode: tables ensured")

    yield  # ------- app chal raha hai yahan -------

    logger.info("Shutting down app")


def create_app() -> FastAPI:
    """
    Application factory.

    Why factory pattern:
    - Tests me alag config ke saath app bana sakte hain
    - Multiple apps (e.g., admin + public) same code se ban sakte hain
    - Global state se bachte hain
    """
    app = FastAPI(
        title="Multi-Vendor Marketplace",
        version="0.1.0",
        debug=settings.DEBUG,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Middleware (order matters: outermost first)
    add_request_id_middleware(app)

    # Exception handlers
    register_exception_handlers(app)

    # Routers
    app.include_router(health.router, prefix="/api/v1")
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(buyers.router, prefix="/api/v1")
    app.include_router(sellers.router, prefix="/api/v1")
    return app


app = create_app()
