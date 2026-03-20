"""Тест SC001 — Создание продукта из текстовой идеи.

## Трассируемость
Feature: F001 — Product Creation & Discovery
Scenario: SC001 — User submits product idea text

## BDD
Given: User is authenticated
When:  User submits product idea text
Then:  System creates product draft and returns clarification questions
"""
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.app.service.product.discovery_service import DiscoveryService, DISCOVERY_QUESTIONS


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_data, expected",
    [
        (
            {"idea_text": "A Telegram bot for fitness tracking"},
            {"is_complete": False, "has_questions": True},
        ),
        (
            {"idea_text": "A bot for scheduling meetings"},
            {"is_complete": False, "has_questions": True},
        ),
    ],
    ids=["fitness_bot_idea", "scheduling_bot_idea"],
)
async def test_create_product_returns_product_and_questions(
    discovery_service, mock_session, input_data, expected
):
    """
    Given: User is authenticated
    When:  User submits product idea text
    Then:  System creates product draft and returns follow-up questions
    """
    # Given
    mock_product = MagicMock()
    mock_product.id = uuid.uuid4()
    mock_product.idea_text = input_data["idea_text"]
    mock_product.status = "discovery_in_progress"

    # When
    with patch.object(
        discovery_service.product_repo, "create",
        new_callable=AsyncMock, return_value=mock_product,
    ):
        with patch.object(
            discovery_service.product_repo, "update_status",
            new_callable=AsyncMock, return_value=mock_product,
        ):
            result = await discovery_service.create_product(input_data["idea_text"])

    # Then
    assert "product" in result
    assert "follow_up_questions" in result
    assert len(result["follow_up_questions"]) > 0
    assert result["is_complete"] is expected["is_complete"]


@pytest.mark.asyncio
async def test_create_product_returns_first_three_questions(discovery_service, mock_session):
    """
    Given: User is authenticated
    When:  User submits product idea text
    Then:  System returns first 3 discovery questions
    """
    mock_product = MagicMock()
    mock_product.status = "draft"

    with patch.object(
        discovery_service.product_repo, "create",
        new_callable=AsyncMock, return_value=mock_product,
    ):
        with patch.object(
            discovery_service.product_repo, "update_status",
            new_callable=AsyncMock, return_value=mock_product,
        ):
            result = await discovery_service.create_product("A bot for scheduling meetings")

    assert result["follow_up_questions"] == DISCOVERY_QUESTIONS[:3]
