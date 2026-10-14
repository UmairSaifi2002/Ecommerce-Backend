from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    Why DeclarativeBase (SQLAlchemy 2.0 style):
    - Modern approach, replaces declarative_base() function
    - Supports type hints natively (Mapped[int], mapped_column)
    - Better IDE support and type checking

    Every model will inherit from this:
        class User(Base): ...
    """

    # pass
