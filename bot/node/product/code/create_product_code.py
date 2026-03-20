"""CreateProductCode — calls backend API to create product.

## Трассируемость
Feature: F001 — Product Creation & Discovery
Scenarios: UC-1.1
"""
from aiogram.fsm.context import FSMContext

from bot.service.api.products_api import ProductsAPI


class CreateProductCode:
    def __init__(self):
        self._api = ProductsAPI()

    async def run(self, trigger_data: dict, state: FSMContext) -> dict:
        idea_text = trigger_data["idea_text"]
        if not idea_text or len(idea_text) < 10:
            return {"answer_name": "idea_too_short", "data": {}}

        try:
            result = await self._api.create_product(idea_text)
        except Exception as e:
            return {"answer_name": "error", "data": {"error": str(e)}}

        product = result.get("product", {})
        questions = result.get("follow_up_questions", [])

        await state.update_data(
            product_id=product.get("id"),
            pending_questions=questions,
            current_question_idx=0,
        )

        if questions:
            return {
                "answer_name": "product_created_with_questions",
                "data": {"first_question": questions[0]},
            }
        return {"answer_name": "product_created", "data": {}}
