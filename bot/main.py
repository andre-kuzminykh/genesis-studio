"""Telegram bot entry point for Genesis Studio.

Product: P001 — PRD-first platform
Bot = UI only layer. All data and logic via backend HTTP API.
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from bot.core.config import bot_settings
from bot.widgets.start_widget import router as start_router
from bot.widgets.product_widget import router as product_router
from bot.widgets.feature_widget import router as feature_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token=bot_settings.telegram_bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    # Register widget routers
    dp.include_router(start_router)
    dp.include_router(product_router)
    dp.include_router(feature_router)

    logger.info("Genesis Studio bot starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
