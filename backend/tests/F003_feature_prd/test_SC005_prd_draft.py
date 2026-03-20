"""Тест SC005 — PRD draft generation.

## Трассируемость
Feature: F003 — Feature PRD Generator
Scenario: SC005 — User requests PRD draft generation

## BDD
Given: Feature exists with approved feature map
When:  User requests PRD draft generation
Then:  System creates PRD version with user stories and business rules
"""
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.app.service.feature.prd_service import PRDService


@pytest.mark.asyncio
async def test_generate_prd_draft_creates_version(prd_service, mock_feature):
    """
    Given: Feature exists with approved feature map
    When:  User requests PRD draft generation
    Then:  PRD version and user stories are created
    """
    # Given
    mock_prd = MagicMock()
    mock_prd.id = uuid.uuid4()
    mock_prd.version_number = 1

    # When
    with patch.object(prd_service.feature_repo, "get_by_id", new_callable=AsyncMock, return_value=mock_feature):
        with patch.object(prd_service.prd_repo, "create_prd_version", new_callable=AsyncMock, return_value=mock_prd):
            with patch.object(prd_service.prd_repo, "bulk_create_stories", new_callable=AsyncMock, return_value=[]):
                with patch.object(prd_service.feature_repo, "update_status", new_callable=AsyncMock):
                    result = await prd_service.generate_prd_draft(mock_feature.id)

    # Then
    assert "prd_version" in result
    assert "user_stories" in result


@pytest.mark.asyncio
async def test_generate_prd_draft_feature_not_found(prd_service):
    """
    Given: Feature does not exist
    When:  User requests PRD draft generation
    Then:  ValueError is raised
    """
    with patch.object(prd_service.feature_repo, "get_by_id", new_callable=AsyncMock, return_value=None):
        with pytest.raises(ValueError, match="not found"):
            await prd_service.generate_prd_draft(uuid.uuid4())


@pytest.mark.asyncio
async def test_get_traceability_returns_counts(prd_service, mock_prd_version):
    """
    Given: Feature has a current PRD version
    When:  User requests traceability graph
    Then:  Counts of all artifacts are returned
    """
    with patch.object(prd_service.prd_repo, "get_current_prd_version", new_callable=AsyncMock, return_value=mock_prd_version):
        with patch.object(prd_service.prd_repo, "get_links_for_prd", new_callable=AsyncMock, return_value=[]):
            result = await prd_service.get_traceability(uuid.uuid4())

    assert "user_stories_count" in result
    assert "use_cases_count" in result
    assert "requirements_count" in result
    assert "test_cases_count" in result
    assert "links" in result
