"""Start widget — handles /start command and main menu.

Feature: F001 Product Creation & Discovery
Architecture: Widget → Trigger → Code → Answer
Bot = UI only; all data via backend API.
"""
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.main_kb import main_menu_keyboard

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Trigger: /start command."""
    await message.answer(
        "Welcome to Genesis Studio!\n\n"
        "I help you create products through a PRD-first workflow:\n"
        "idea → discovery → features → PRD → UX → use cases → "
        "requirements → tests → code → GitHub → deploy\n\n"
        "Choose an action below:",
        reply_markup=main_menu_keyboard(),
    )
