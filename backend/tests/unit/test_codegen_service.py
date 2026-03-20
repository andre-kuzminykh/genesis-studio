"""Unit tests for CodegenService.

Feature: F013 Backend Code Generator, F014 Telegram Bot Code Generator
Scenario: UC-4.1
"""
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.app.services.codegen_service import CodegenService, CODEGEN_POLICY


@pytest.fixture
def codegen_service(mock_session):
    return CodegenService(mock_session)


class TestCodegenPolicy:
    """Tests for Section 7 — Mandatory Architectural Codegen Policy."""

    def test_policy_defines_bot_as_ui_only(self):
        assert "UI only" in CODEGEN_POLICY["bot_role"]

    def test_policy_defines_backend_as_data_source(self):
        assert "data and business logic" in CODEGEN_POLICY["backend_role"]

    def test_policy_requires_prd_json(self):
        assert "prd.json" in CODEGEN_POLICY["prd_json"]

    def test_policy_requires_tests(self):
        assert "test coverage" in CODEGEN_POLICY["tests_required"]

    def test_policy_requires_traceability(self):
        assert "Feature" in CODEGEN_POLICY["traceability"]

    def test_policy_requires_approved_prd(self):
        assert "approved PRD version" in CODEGEN_POLICY["changes_from_approved_only"]


class TestGenerateCode:
    """Tests for UC-4.1 — code generation from approved PRD."""

    async def test_generate_code_requires_approved_prd(self, codegen_service):
        """Code generation must fail if PRD is not approved."""
        mock_feature = MagicMock()
        mock_feature.id = uuid.uuid4()

        mock_prd = MagicMock()
        mock_prd.status = MagicMock()
        mock_prd.status.value = "draft"

        with patch.object(codegen_service.feature_repo, "get_by_id", new_callable=AsyncMock, return_value=mock_feature):
            with patch.object(codegen_service.prd_repo, "get_current_prd_version", new_callable=AsyncMock, return_value=mock_prd):
                with pytest.raises(ValueError, match="must be approved"):
                    await codegen_service.generate_code(mock_feature.id)

    async def test_generate_code_feature_not_found(self, codegen_service):
        with patch.object(codegen_service.feature_repo, "get_by_id", new_callable=AsyncMock, return_value=None):
            with pytest.raises(ValueError, match="not found"):
                await codegen_service.generate_code(uuid.uuid4())
