"""CreateProductTrigger — extracts user idea from message.

## Трассируемость
Feature: F001 — Product Creation & Discovery
Scenarios: UC-1.1
"""
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class CreateProductTrigger:
    async def run(self, message: Message, state: FSMContext) -> dict:
        await state.clear()
        return {"idea_text": message.text, "user_id": message.from_user.id}
