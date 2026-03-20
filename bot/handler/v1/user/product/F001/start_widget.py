"""Widget: Start — handles /start command and main menu.

## Трассируемость
Feature: F001 — Product Creation & Discovery
Scenarios: UC-1.0
"""
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.core.vocab import Vocab
from bot.keyboards.main_kb import main_menu_keyboard

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Trigger: /start command."""
    await message.answer(
        Vocab.WELCOME_TEXT,
        reply_markup=main_menu_keyboard(),
    )
