"""Widget: Create Product — orchestrates product creation flow.

## Трассируемость
Feature: F001 — Product Creation & Discovery
Scenarios: UC-1.1, UC-1.2

UC-1.1 — idea text -> created -> answer: product_created / product_created_with_questions
UC-1.1 — too short -> answer: idea_too_short
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.node.product.trigger.create_product_trigger import CreateProductTrigger
from bot.node.product.code.create_product_code import CreateProductCode
from bot.node.product.answer.product_created_answer import (
    ProductCreatedAnswer,
    ProductCreatedWithQuestionsAnswer,
    IdeaTooShortAnswer,
    ErrorAnswer,
)
from bot.service.api.products_api import ProductsAPI
from bot.keyboards.main_kb import main_menu_keyboard
from bot.core.vocab import Vocab

router = Router(name="create_product")

ANSWER_REGISTRY = {
    "product_created": ProductCreatedAnswer(),
    "product_created_with_questions": ProductCreatedWithQuestionsAnswer(),
    "idea_too_short": IdeaTooShortAnswer(),
    "error": ErrorAnswer(),
}


class ProductCreation(StatesGroup):
    waiting_for_idea = State()
    answering_discovery = State()


@router.message(F.text == Vocab.BTN_CREATE_PRODUCT)
async def handle_start_creation(message: Message, state: FSMContext):
    """Trigger: user taps Create Product button."""
    await state.set_state(ProductCreation.waiting_for_idea)
    await message.answer(Vocab.DESCRIBE_IDEA_TEXT)


@router.message(ProductCreation.waiting_for_idea)
async def handle_create_product(message: Message, state: FSMContext):
    """Widget: Trigger -> Code -> Answer for product creation."""
    trigger = CreateProductTrigger()
    trigger_data = await trigger.run(message, state)

    code = CreateProductCode()
    code_result = await code.run(trigger_data, state)

    answer = ANSWER_REGISTRY[code_result["answer_name"]]
    if code_result["answer_name"] == "product_created_with_questions":
        await state.set_state(ProductCreation.answering_discovery)
    elif code_result["answer_name"] == "product_created":
        await state.clear()

    await answer.run(event=message, user_lang="ru", data=code_result["data"])


@router.message(ProductCreation.answering_discovery)
async def handle_discovery_answer(message: Message, state: FSMContext):
    """Trigger: user answers discovery question."""
    data = await state.get_data()
    product_id = data["product_id"]
    questions = data["pending_questions"]
    idx = data["current_question_idx"]

    current_question = questions[idx] if idx < len(questions) else "General feedback"

    api = ProductsAPI()
    try:
        result = await api.submit_discovery(product_id, current_question, message.text)
    except Exception as e:
        await message.answer(Vocab.ERROR_TEXT.format(error=str(e)))
        return

    is_complete = result.get("is_complete", False)
    next_questions = result.get("follow_up_questions", [])

    if is_complete or not next_questions:
        await state.clear()
        await message.answer(
            Vocab.DISCOVERY_COMPLETE_TEXT,
            reply_markup=main_menu_keyboard(),
        )
    else:
        await state.update_data(
            pending_questions=next_questions,
            current_question_idx=0,
        )
        await message.answer(f"Got it!\n\nQ: {next_questions[0]}")
