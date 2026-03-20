"""Product creation widget — handles product creation and discovery flow.

Feature: F001 Product Creation & Discovery
Architecture: Widget → Trigger → Code → Answer
Bot = UI only; all data via backend API.
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.services.api_client import api_client
from bot.keyboards.main_kb import main_menu_keyboard

router = Router(name="product")


class ProductCreation(StatesGroup):
    waiting_for_idea = State()
    answering_discovery = State()


@router.message(F.text == "Create Product")
async def start_creation(message: Message, state: FSMContext):
    """Trigger: user taps 'Create Product' button."""
    await state.set_state(ProductCreation.waiting_for_idea)
    await message.answer(
        "Describe your product idea in detail.\n"
        "Tell me what problem it solves, who the users are, and what it should do."
    )


@router.message(ProductCreation.waiting_for_idea)
async def receive_idea(message: Message, state: FSMContext):
    """Trigger: user enters product idea text."""
    idea_text = message.text
    if not idea_text or len(idea_text) < 10:
        await message.answer("Please provide a more detailed description (at least 10 characters).")
        return

    try:
        result = await api_client.create_product(idea_text)
    except Exception as e:
        await message.answer(f"Error creating product: {e}")
        await state.clear()
        return

    product = result.get("product", {})
    questions = result.get("follow_up_questions", [])

    await state.update_data(
        product_id=product.get("id"),
        pending_questions=questions,
        current_question_idx=0,
    )

    if questions:
        await state.set_state(ProductCreation.answering_discovery)
        await message.answer(
            f"Product draft created!\n\n"
            f"Now let me ask a few clarification questions.\n\n"
            f"Q: {questions[0]}"
        )
    else:
        await state.clear()
        await message.answer(
            "Product created successfully! Use 'My Products' to view it.",
            reply_markup=main_menu_keyboard(),
        )


@router.message(ProductCreation.answering_discovery)
async def answer_discovery(message: Message, state: FSMContext):
    """Trigger: user answers discovery question."""
    data = await state.get_data()
    product_id = data["product_id"]
    questions = data["pending_questions"]
    idx = data["current_question_idx"]

    current_question = questions[idx] if idx < len(questions) else "General feedback"

    try:
        result = await api_client.submit_discovery(product_id, current_question, message.text)
    except Exception as e:
        await message.answer(f"Error: {e}")
        return

    is_complete = result.get("is_complete", False)
    next_questions = result.get("follow_up_questions", [])

    if is_complete or not next_questions:
        await state.clear()
        await message.answer(
            "Discovery complete! Your product is ready for feature map generation.\n"
            "Use 'My Products' to continue.",
            reply_markup=main_menu_keyboard(),
        )
    else:
        await state.update_data(
            pending_questions=next_questions,
            current_question_idx=0,
        )
        await message.answer(f"Got it!\n\nQ: {next_questions[0]}")
