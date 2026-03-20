"""Code generation service — generates backend and bot code from approved PRD.

Feature: F013 Backend Code Generator, F014 Telegram Bot Code Generator
Scenario: UC-4.1
"""
import hashlib
import json
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.feature import FeatureStatus
from backend.app.repositories.feature_repository import FeatureRepository
from backend.app.repositories.prd_repository import PRDRepository
from backend.app.repositories.git_repository_repo import GitRepositoryRepo

# Mandatory Architectural Codegen Policy (Section 7 of PRD)
CODEGEN_POLICY = {
    "bot_role": "UI only — no DB access, no ORM, no migrations, no heavy computation",
    "backend_role": "Source of data and business logic — all data, rules, integrations",
    "prd_json": "Each project contains prd.json at root — PRD is source of truth",
    "codegen_order": "PRD → project detection → gap analysis → tasks → tests → backend code → bot code",
    "backend_arch": "API → Service → Repository → Model (strictly top-down)",
    "bot_arch": "Widget → Trigger → Code → Answer (API access only through service/api clients)",
    "tests_required": "Every scenario_id from PRD must have test coverage",
    "traceability": "Every module must contain docstring with Feature / Scenario references",
    "changes_from_approved_only": "Code changes only from approved PRD version",
    "change_flow": "New PRD version + Change Request + test refresh before code regen",
}


class CodegenService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.feature_repo = FeatureRepository(session)
        self.prd_repo = PRDRepository(session)
        self.git_repo = GitRepositoryRepo(session)

    async def generate_code(
        self, feature_id: uuid.UUID, target_branch: str = "main", commit_message: str | None = None
    ) -> dict:
        """Generate backend and bot code for a feature.

        Enforces mandatory architectural codegen policy.
        Scenario: UC-4.1
        """
        feature = await self.feature_repo.get_by_id(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")

        prd = await self.prd_repo.get_current_prd_version(feature_id)
        if not prd:
            raise ValueError("No current PRD version found")

        if prd.status.value != "approved":
            raise ValueError("PRD version must be approved before code generation")

        # Build prd.json content
        prd_json = {
            "feature_id": feature.feature_id,
            "feature_name": feature.name,
            "version": prd.version_number,
            "content": prd.content,
            "codegen_policy": CODEGEN_POLICY,
            "use_cases": [
                {"use_case_id": uc.use_case_id, "title": uc.title}
                for uc in prd.use_cases
            ],
            "requirements": [
                {"req_id": req.req_id, "title": req.title, "type": req.req_type.value}
                for req in prd.requirements
            ],
            "test_cases": [
                {"test_id": tc.test_id, "title": tc.title, "scenario_id": tc.scenario_id}
                for tc in prd.test_cases
            ],
        }

        # Generate backend artifacts
        backend_artifacts = self._generate_backend_artifacts(feature, prd, prd_json)
        # Generate bot artifacts
        bot_artifacts = self._generate_bot_artifacts(feature, prd, prd_json)
        # Generate prd.json
        prd_json_artifact = {
            "file_path": "prd.json",
            "content": json.dumps(prd_json, indent=2, ensure_ascii=False),
            "artifact_type": "config",
            "description": "PRD source of truth for feature",
        }

        all_artifacts = [prd_json_artifact] + backend_artifacts + bot_artifacts

        # Store code artifact metadata
        for artifact_data in all_artifacts:
            content_hash = hashlib.sha256(artifact_data["content"].encode()).hexdigest()
            await self.git_repo.create_code_artifact(
                feature_id=feature_id,
                prd_version_id=prd.id,
                artifact_type=artifact_data["artifact_type"],
                file_path=artifact_data["file_path"],
                content_hash=content_hash,
                description=artifact_data.get("description"),
            )

        await self.feature_repo.update_status(feature, FeatureStatus.code_generated)
        await self.session.commit()

        return {
            "feature_id": feature_id,
            "prd_version_id": prd.id,
            "artifacts_count": len(all_artifacts),
            "commit_sha": None,
            "push_status": "pending",
            "generation_report": {
                "backend_files": len(backend_artifacts),
                "bot_files": len(bot_artifacts),
                "total_files": len(all_artifacts),
                "codegen_policy_applied": True,
                "artifacts": [
                    {"path": a["file_path"], "type": a["artifact_type"]}
                    for a in all_artifacts
                ],
            },
        }

    def _generate_backend_artifacts(self, feature, prd, prd_json) -> list[dict]:
        """Generate FastAPI backend code following architectural policy.

        Backend architecture: API → Service → Repository → Model
        """
        feature_slug = feature.feature_id.lower().replace("-", "_")
        artifacts = []

        # Model
        artifacts.append({
            "file_path": f"backend/app/models/{feature_slug}.py",
            "content": (
                f'"""Model for {feature.name}.\n\n'
                f"Feature: {feature.feature_id}\n"
                f'"""\n'
                f"# Auto-generated from PRD v{prd.version_number}\n"
                f"# Codegen policy: {CODEGEN_POLICY['backend_arch']}\n\n"
                f"from sqlalchemy import Column, String, Text\n"
                f"from sqlalchemy.dialects.postgresql import UUID\n"
                f"from backend.app.core.database import Base\n\n\n"
                f"class {feature.name.replace(' ', '')}(Base):\n"
                f"    __tablename__ = '{feature_slug}s'\n"
                f"    # TODO: Define columns from PRD requirements\n"
                f"    pass\n"
            ),
            "artifact_type": "backend",
            "description": f"SQLAlchemy model for {feature.name}",
        })

        # Repository
        artifacts.append({
            "file_path": f"backend/app/repositories/{feature_slug}_repository.py",
            "content": (
                f'"""Repository for {feature.name}.\n\n'
                f"Feature: {feature.feature_id}\n"
                f'"""\n'
                f"from sqlalchemy.ext.asyncio import AsyncSession\n\n\n"
                f"class {feature.name.replace(' ', '')}Repository:\n"
                f"    def __init__(self, session: AsyncSession):\n"
                f"        self.session = session\n"
                f"    # TODO: Implement CRUD from PRD requirements\n"
            ),
            "artifact_type": "backend",
            "description": f"Repository for {feature.name}",
        })

        # Service
        artifacts.append({
            "file_path": f"backend/app/services/{feature_slug}_service.py",
            "content": (
                f'"""Service for {feature.name}.\n\n'
                f"Feature: {feature.feature_id}\n"
                f'"""\n'
                f"from sqlalchemy.ext.asyncio import AsyncSession\n\n\n"
                f"class {feature.name.replace(' ', '')}Service:\n"
                f"    def __init__(self, session: AsyncSession):\n"
                f"        self.session = session\n"
                f"    # TODO: Implement business logic from PRD use cases\n"
            ),
            "artifact_type": "backend",
            "description": f"Service for {feature.name}",
        })

        # API endpoint
        artifacts.append({
            "file_path": f"backend/app/api/v1/{feature_slug}.py",
            "content": (
                f'"""API endpoints for {feature.name}.\n\n'
                f"Feature: {feature.feature_id}\n"
                f'"""\n'
                f"from fastapi import APIRouter, Depends\n\n"
                f"router = APIRouter(prefix='/{feature_slug}', tags=['{feature.name}'])\n\n"
                f"# TODO: Implement endpoints from PRD requirements\n"
            ),
            "artifact_type": "backend",
            "description": f"API endpoints for {feature.name}",
        })

        # Tests
        artifacts.append({
            "file_path": f"backend/tests/test_{feature_slug}.py",
            "content": (
                f'"""Tests for {feature.name}.\n\n'
                f"Feature: {feature.feature_id}\n"
                f'"""\n'
                f"import pytest\n\n\n"
                + "\n\n".join(
                    f"async def test_{tc.test_id.lower().replace('-', '_')}():\n"
                    f'    """Scenario: {tc.scenario_id or "N/A"} — {tc.title}"""\n'
                    f"    # TODO: Implement test\n"
                    f"    pass\n"
                    for tc in prd.test_cases
                )
            ),
            "artifact_type": "test",
            "description": f"Test suite for {feature.name}",
        })

        return artifacts

    def _generate_bot_artifacts(self, feature, prd, prd_json) -> list[dict]:
        """Generate aiogram 3 bot code following architectural policy.

        Bot architecture: Widget → Trigger → Code → Answer
        Bot = UI only, no DB access.
        """
        feature_slug = feature.feature_id.lower().replace("-", "_")
        artifacts = []

        # Widget handler
        artifacts.append({
            "file_path": f"bot/widgets/{feature_slug}_widget.py",
            "content": (
                f'"""Telegram widget for {feature.name}.\n\n'
                f"Feature: {feature.feature_id}\n"
                f"Architecture: Widget → Trigger → Code → Answer\n"
                f"Bot = UI only; all data via backend API.\n"
                f'"""\n'
                f"from aiogram import Router\n"
                f"from aiogram.types import Message, CallbackQuery\n\n"
                f"router = Router(name='{feature_slug}')\n\n\n"
                f"@router.message()\n"
                f"async def handle_{feature_slug}(message: Message):\n"
                f'    """Trigger: user message for {feature.name}."""\n'
                f"    # TODO: Call backend API and render response\n"
                f'    await message.answer("Feature {feature.name} — coming soon")\n'
            ),
            "artifact_type": "bot",
            "description": f"Telegram widget for {feature.name}",
        })

        # Keyboard layouts
        artifacts.append({
            "file_path": f"bot/keyboards/{feature_slug}_kb.py",
            "content": (
                f'"""Keyboards for {feature.name}.\n\n'
                f"Feature: {feature.feature_id}\n"
                f'"""\n'
                f"from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton\n\n\n"
                f"def get_{feature_slug}_keyboard() -> InlineKeyboardMarkup:\n"
                f"    return InlineKeyboardMarkup(inline_keyboard=[\n"
                f"        [InlineKeyboardButton(text='Action 1', callback_data='{feature_slug}_action_1')],\n"
                f"        [InlineKeyboardButton(text='Action 2', callback_data='{feature_slug}_action_2')],\n"
                f"    ])\n"
            ),
            "artifact_type": "bot",
            "description": f"Keyboards for {feature.name}",
        })

        return artifacts
