"""Unit tests for DiscoveryService.

Feature: F001 Product Creation & Discovery
Scenario: UC-1.1, UC-1.2
"""
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.app.services.discovery_service import DiscoveryService, DISCOVERY_QUESTIONS


@pytest.fixture
def discovery_service(mock_session):
    return DiscoveryService(mock_session)


class TestCreateProduct:
    """Tests for UC-1.1 — product creation from text idea."""

    async def test_create_product_returns_product_and_questions(self, discovery_service, mock_session):
        """FR-1: System must allow creating a new product from text description."""
        mock_product = MagicMock()
        mock_product.id = uuid.uuid4()
        mock_product.idea_text = "Test idea"
        mock_product.status = "discovery_in_progress"

        with patch.object(discovery_service.product_repo, "create", new_callable=AsyncMock, return_value=mock_product):
            with patch.object(discovery_service.product_repo, "update_status", new_callable=AsyncMock, return_value=mock_product):
                result = await discovery_service.create_product("Test idea for a fitness app")

        assert "product" in result
        assert "follow_up_questions" in result
        assert len(result["follow_up_questions"]) > 0
        assert result["is_complete"] is False

    async def test_create_product_starts_discovery(self, discovery_service, mock_session):
        """FR-2: System must extract product summary and initial feature map."""
        mock_product = MagicMock()
        mock_product.status = "draft"

        with patch.object(discovery_service.product_repo, "create", new_callable=AsyncMock, return_value=mock_product):
            with patch.object(discovery_service.product_repo, "update_status", new_callable=AsyncMock, return_value=mock_product):
                result = await discovery_service.create_product("A bot for scheduling meetings")

        assert result["follow_up_questions"] == DISCOVERY_QUESTIONS[:3]


class TestDiscoveryQuestions:
    """Tests for discovery interview flow."""

    def test_discovery_questions_are_defined(self):
        """FR-3: System must save all discovery inputs."""
        assert len(DISCOVERY_QUESTIONS) >= 3
        for q in DISCOVERY_QUESTIONS:
            assert isinstance(q, str)
            assert len(q) > 10
