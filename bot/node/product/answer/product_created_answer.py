"""ProductCreatedAnswer — shows product creation success.

## Трассируемость
Feature: F001 — Product Creation & Discovery
Scenarios: UC-1.1
"""
from aiogram.types import Message

from bot.core.vocab import Vocab
from bot.keyboards.main_kb import main_menu_keyboard


class ProductCreatedAnswer:
    async def run(self, event: Message, user_lang: str = "ru", data: dict | None = None):
        await event.answer(
            Vocab.PRODUCT_CREATED_TEXT,
            reply_markup=main_menu_keyboard(),
        )


class ProductCreatedWithQuestionsAnswer:
    async def run(self, event: Message, user_lang: str = "ru", data: dict | None = None):
        question = data.get("first_question", "") if data else ""
        await event.answer(
            f"{Vocab.PRODUCT_CREATED_TEXT}\n\n"
            f"Now let me ask a few clarification questions.\n\n"
            f"Q: {question}"
        )


class IdeaTooShortAnswer:
    async def run(self, event: Message, user_lang: str = "ru", data: dict | None = None):
        await event.answer(Vocab.IDEA_TOO_SHORT_TEXT)


class ErrorAnswer:
    async def run(self, event: Message, user_lang: str = "ru", data: dict | None = None):
        error = data.get("error", "Unknown error") if data else "Unknown error"
        await event.answer(Vocab.ERROR_TEXT.format(error=error))
