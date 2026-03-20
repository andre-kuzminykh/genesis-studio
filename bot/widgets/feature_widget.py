"""Feature widget — handles feature-level operations and PRD workflow.

Feature: F002-F015
Architecture: Widget → Trigger → Code → Answer
Bot = UI only; all data via backend API.
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.services.api_client import api_client
from bot.keyboards.main_kb import feature_actions_keyboard

router = Router(name="feature")


@router.callback_query(F.data.startswith("prd_draft:"))
async def generate_prd_draft(callback: CallbackQuery):
    """Trigger: user requests PRD draft generation."""
    feature_id = callback.data.split(":")[1]
    await callback.answer("Generating PRD draft...")
    try:
        result = await api_client.generate_prd_draft(feature_id)
        await callback.message.answer(
            f"PRD Draft generated!\n"
            f"Version: {result.get('version_number', 1)}\n"
            f"Summary: {result.get('summary', 'N/A')}\n\n"
            f"Choose next action:",
            reply_markup=feature_actions_keyboard(feature_id),
        )
    except Exception as e:
        await callback.message.answer(f"Error: {e}")


@router.callback_query(F.data.startswith("gen_ux:"))
async def generate_ux(callback: CallbackQuery):
    """Trigger: user requests UX preview generation."""
    feature_id = callback.data.split(":")[1]
    await callback.answer("Generating UX preview...")
    try:
        flows = await api_client.generate_ux(feature_id)
        text = "UX Previews generated:\n\n"
        for flow in flows:
            text += f"--- {flow.get('title', 'Untitled')} ---\n"
            text += f"{flow.get('content', '')}\n\n"
        await callback.message.answer(text[:4000])
    except Exception as e:
        await callback.message.answer(f"Error: {e}")


@router.callback_query(F.data.startswith("gen_uc:"))
async def generate_use_cases(callback: CallbackQuery):
    """Trigger: user requests use case generation."""
    feature_id = callback.data.split(":")[1]
    await callback.answer("Generating use cases...")
    try:
        cases = await api_client.generate_use_cases(feature_id)
        text = "Use Cases generated:\n\n"
        for uc in cases:
            text += (
                f"[{uc.get('use_case_id')}] {uc.get('title')}\n"
                f"Given: {uc.get('given')}\n"
                f"When: {uc.get('when')}\n"
                f"Then: {uc.get('then')}\n\n"
            )
        await callback.message.answer(text[:4000])
    except Exception as e:
        await callback.message.answer(f"Error: {e}")


@router.callback_query(F.data.startswith("gen_req:"))
async def generate_requirements(callback: CallbackQuery):
    """Trigger: user requests requirements derivation."""
    feature_id = callback.data.split(":")[1]
    await callback.answer("Deriving requirements...")
    try:
        reqs = await api_client.generate_requirements(feature_id)
        text = "Requirements derived:\n\n"
        for r in reqs:
            text += f"[{r.get('req_id')}] ({r.get('req_type')}) {r.get('title')}\n"
        await callback.message.answer(text[:4000])
    except Exception as e:
        await callback.message.answer(f"Error: {e}")


@router.callback_query(F.data.startswith("gen_tests:"))
async def generate_tests(callback: CallbackQuery):
    """Trigger: user requests test generation."""
    feature_id = callback.data.split(":")[1]
    await callback.answer("Generating tests...")
    try:
        tests = await api_client.generate_tests(feature_id)
        text = "Test Cases generated:\n\n"
        for tc in tests:
            text += f"[{tc.get('test_id')}] {tc.get('title')} ({tc.get('test_type')})\n"
        await callback.message.answer(text[:4000])
    except Exception as e:
        await callback.message.answer(f"Error: {e}")


@router.callback_query(F.data.startswith("gen_code:"))
async def generate_code(callback: CallbackQuery):
    """Trigger: user requests code generation."""
    feature_id = callback.data.split(":")[1]
    await callback.answer("Generating code...")
    try:
        result = await api_client.generate_code(feature_id)
        report = result.get("generation_report", {})
        await callback.message.answer(
            f"Code generated!\n"
            f"Backend files: {report.get('backend_files', 0)}\n"
            f"Bot files: {report.get('bot_files', 0)}\n"
            f"Total: {report.get('total_files', 0)}\n\n"
            f"Choose next action:",
            reply_markup=feature_actions_keyboard(feature_id),
        )
    except Exception as e:
        await callback.message.answer(f"Error: {e}")


@router.callback_query(F.data.startswith("push_gh:"))
async def push_to_github(callback: CallbackQuery):
    """Trigger: user requests GitHub push."""
    feature_id = callback.data.split(":")[1]
    await callback.answer("Pushing to GitHub...")
    try:
        result = await api_client.push_to_github(feature_id)
        await callback.message.answer(
            f"Pushed to GitHub!\n"
            f"Branch: {result.get('branch')}\n"
            f"Commit: {result.get('commit_sha', 'N/A')}\n"
            f"Status: {result.get('status')}"
        )
    except Exception as e:
        await callback.message.answer(f"Error: {e}")


@router.callback_query(F.data.startswith("deploy:"))
async def deploy_local(callback: CallbackQuery):
    """Trigger: user requests local deployment."""
    feature_id = callback.data.split(":")[1]
    await callback.answer("Deploying locally...")
    try:
        result = await api_client.deploy_local(feature_id)
        endpoints = result.get("endpoints", {})
        ep_text = "\n".join(f"  {k}: {v}" for k, v in endpoints.items()) if endpoints else "  None"
        await callback.message.answer(
            f"Deployment status: {result.get('status')}\n"
            f"Endpoints:\n{ep_text}\n\n"
            f"{result.get('logs', '')}"
        )
    except Exception as e:
        await callback.message.answer(f"Error: {e}")
