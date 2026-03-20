"""Тест SC020 — Change request creation and impact analysis.

## Трассируемость
Feature: F011 — PRD Versioning & Change Requests
Scenario: SC020 — User creates change request for feature

## BDD
Given: Feature exists with approved PRD version
When:  User submits change request
Then:  System creates CR, calculates impact, returns affected artifact counts
"""
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.app.service.feature.change_request_service import ChangeRequestService


@pytest.mark.asyncio
async def test_create_cr_calculates_impact(cr_service, mock_feature, mock_prd_with_artifacts):
    """
    Given: Feature has current PRD with 2 use cases, 1 req, 3 tests
    When:  User creates change request
    Then:  Impact analysis shows correct artifact counts
    """
    mock_cr = MagicMock()
    mock_cr.id = uuid.uuid4()
    mock_cr.impact_analysis = None
    mock_cr.diff_summary = None

    with patch.object(cr_service.feature_repo, "get_by_id", new_callable=AsyncMock, return_value=mock_feature):
        with patch.object(cr_service.prd_repo, "get_current_prd_version", new_callable=AsyncMock, return_value=mock_prd_with_artifacts):
            with patch.object(cr_service.prd_repo, "create_change_request", new_callable=AsyncMock, return_value=mock_cr):
                result = await cr_service.create_change_request(
                    mock_feature.id, "Update validation", "Add email validation"
                )

    assert "change_request" in result
    assert "impact_analysis" in result
    impact = result["impact_analysis"]
    assert impact["affected_use_cases"] == 2
    assert impact["affected_requirements"] == 1
    assert impact["affected_tests"] == 3


@pytest.mark.asyncio
async def test_create_cr_feature_not_found(cr_service):
    """
    Given: Feature does not exist
    When:  User creates change request
    Then:  ValueError raised
    """
    with patch.object(cr_service.feature_repo, "get_by_id", new_callable=AsyncMock, return_value=None):
        with pytest.raises(ValueError, match="not found"):
            await cr_service.create_change_request(uuid.uuid4(), "title", "desc")
