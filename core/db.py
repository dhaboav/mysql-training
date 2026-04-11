"""Database Configuration FastAPI application.

This module provides configuration for database connection in application.

Features:
    - Database session dependency injection.
    - close_db: Closing database connection.
"""

from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session, create_engine

from .config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_db() -> Generator[Session, None, None]:
    """Get a database session for dependency injection."""

    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


def close_db() -> None:
    """Close the database connection."""
    engine.dispose()


SessionDep = Annotated[Session, Depends(get_db)]
