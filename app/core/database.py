from functools import lru_cache
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


def get_engine():
    settings = get_settings()

    Path(settings.database_path).parent.mkdir(parents=True, exist_ok=True)

    return create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
        echo=settings.debug,
    )


@lru_cache
def get_engine_cached():
    return get_engine()


@lru_cache
def get_session_maker():
    return sessionmaker(
        bind=get_engine_cached(),
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=Session,
    )


SessionLocal = get_session_maker()


def get_db() -> Generator[Session, None, None]:
    """Provide a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
