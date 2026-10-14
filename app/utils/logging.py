import logging
import sys

from app.config.settings import settings


def setup_logging() -> None:
    """
    Configure root logger once at app startup.

    Format: timestamp | level | module | message
    In dev: DEBUG level. In prod: INFO level.
    """
    level = logging.DEBUG if settings.DEBUG else logging.INFO

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    # Avoid duplicate handlers if setup called twice (e.g., reload)
    root.handlers = [handler]

    # Quiet down noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.DEBUG else logging.WARNING
    )
    logging.getLogger("aiosqlite").setLevel(logging.WARNING)
