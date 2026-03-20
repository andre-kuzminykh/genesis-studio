"""Тест SC010 — Codegen policy validation.

## Трассируемость
Feature: F013 — Backend Code Generator, F014 — Telegram Bot Code Generator
Scenario: SC010 — Mandatory architectural codegen policy

## BDD
Given: Codegen policy is defined
When:  Checking policy keys
Then:  All mandatory policies are present and correct
"""
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.app.service.feature.codegen_service import CodegenService, CODEGEN_POLICY


class TestCodegenPolicy:
    """Tests for mandatory architectural codegen policy."""

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


@pytest.mark.asyncio
async def test_generate_code_requires_approved_prd(codegen_service):
    """
    Given: PRD version exists in draft status
    When:  User requests code generation
    Then:  ValueError raised because PRD must be approved
    """
    mock_feature = MagicMock()
    mock_feature.id = uuid.uuid4()

    mock_prd = MagicMock()
    mock_prd.status = MagicMock()
    mock_prd.status.value = "draft"

    with patch.object(codegen_service.feature_repo, "get_by_id", new_callable=AsyncMock, return_value=mock_feature):
        with patch.object(codegen_service.prd_repo, "get_current_prd_version", new_callable=AsyncMock, return_value=mock_prd):
            with pytest.raises(ValueError, match="must be approved"):
                await codegen_service.generate_code(mock_feature.id)


@pytest.mark.asyncio
async def test_generate_code_feature_not_found(codegen_service):
    """
    Given: Feature does not exist
    When:  User requests code generation
    Then:  ValueError raised
    """
    with patch.object(codegen_service.feature_repo, "get_by_id", new_callable=AsyncMock, return_value=None):
        with pytest.raises(ValueError, match="not found"):
            await codegen_service.generate_code(uuid.uuid4())
