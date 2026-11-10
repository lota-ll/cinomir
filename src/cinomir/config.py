"""Конфігурація лише через змінні оточення (12-factor, принцип III)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


def _int_set(raw: str) -> frozenset[int]:
    """'111, 222,,333' -> frozenset({111, 222, 333})"""
    return frozenset(int(x) for x in raw.replace(" ", "").split(",") if x)


@dataclass(frozen=True)
class Settings:
    database_url: str
    redis_url: str
    log_level: str
    telegram_bot_token: str
    allowed_user_ids: frozenset[int]

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            database_url=os.getenv(
                "DATABASE_URL", "postgresql+psycopg://cinomir:cinomir@localhost:5432/cinomir"
            ),
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
            allowed_user_ids=_int_set(os.getenv("ALLOWED_USER_IDS", "")),
        )


@lru_cache
def get_settings() -> Settings:
    return Settings.from_env()
