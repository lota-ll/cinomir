"""Живий димовий тест: по одному запиту в кожну мережу. НЕ частина pytest.

Запуск: PYTHONPATH=src .venv/bin/python scripts/smoke_chains.py "тунець у власному соку"
Код виходу 0 — усі мережі відповіли; 1 — хоч одна впала (придатно для CI/cron).
"""

from __future__ import annotations

import asyncio
import sys

import httpx

from cinomir.chains import build_chains
from cinomir.config import get_settings
from cinomir.matching import main_word, relevance


async def main(query: str) -> int:
    s = get_settings()
    failed = 0
    async with httpx.AsyncClient(
        headers={"User-Agent": s.user_agent},
        timeout=s.chain_timeout_seconds + 2,
        follow_redirects=True,
    ) as client:
        for name, chain in build_chains(s).items():
            try:
                offers = await chain.search(client, main_word(query), s.search_limit_per_chain)
            except Exception as e:  # діагностика: показуємо будь-яку причину
                print(f"{name:6} FAIL {type(e).__name__}: {e}")
                failed += 1
                continue
            ok = [o for o in offers if relevance(query, o.title) >= 0.6]
            print(f"{name:6} OK   всього={len(offers)} релевантних={len(ok)}")
            for o in ok[:3]:
                print(f"         {o.price:>7.2f} {o.pack_raw or '-':8} {o.title[:60]}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main(" ".join(sys.argv[1:]) or "тунець у власному соку")))
