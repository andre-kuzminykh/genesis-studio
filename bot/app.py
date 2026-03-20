"""Telegram bot entry point for Genesis Studio.

## Трассируемость
Feature: P001 — PRD-first платформа
"""
import asyncio
import logging

from bot.core.loader import bot, dp
from bot.handler.include_router import register_routers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    register_routers(dp)
    logger.info("Genesis Studio bot starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
