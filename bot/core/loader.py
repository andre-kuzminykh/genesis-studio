"""Bot and Dispatcher initialization.

## Трассируемость
Feature: P001 — PRD-first платформа
"""
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from bot.core.config import bot_settings

bot = Bot(token=bot_settings.telegram_bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher()
