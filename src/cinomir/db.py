"""Async SQLAlchemy."""

from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from .config import get_settings


class Base(DeclarativeBase):
    pass


def utcnow() -> datetime:
    return datetime.now(UTC)


_engine: AsyncEngine | None = None
_factory: async_sessionmaker[AsyncSession] | None = None


def configure_db(url: str) -> AsyncEngine:
    global _engine, _factory
    _engine = create_async_engine(url, pool_pre_ping=True)
    _factory = async_sessionmaker(_engine, expire_on_commit=False)
    return _engine


def session_factory() -> async_sessionmaker[AsyncSession]:
    if _factory is None:
        configure_db(get_settings().database_url)
    assert _factory is not None
    return _factory


async def get_session() -> AsyncIterator[AsyncSession]:
    async with session_factory()() as session:
        yield session


async def dispose() -> None:
    if _engine is not None:
        await _engine.dispose()
