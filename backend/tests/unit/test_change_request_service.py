"""Unit tests for ChangeRequestService.

Feature: F011 PRD Versioning & Change Requests
Scenario: UC-5.1
"""
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.app.services.change_request_service import ChangeRequestService


@pytest.fixture
def cr_service(mock_session):
    return ChangeRequestService(mock_session)


@pytest.fixture
def mock_feature():
    f = MagicMock()
    f.id = uuid.uuid4()
    return f


@pytest.fixture
def mock_prd_with_artifacts():
    prd = MagicMock()
    prd.id = uuid.uuid4()
    prd.version_number = 1
    prd.content = {"feature_id": "F001"}
    prd.use_cases = [MagicMock(), MagicMock()]
    prd.requirements = [MagicMock()]
    prd.test_cases = [MagicMock(), MagicMock(), MagicMock()]
    prd.tasks = [MagicMock()]
    return prd


class TestCreateChangeRequest:
    """Tests for UC-5.1 — change request creation and impact analysis."""

    async def test_create_cr_calculates_impact(self, cr_service, mock_feature, mock_prd_with_artifacts):
        """FR-19: System must automatically calculate impact scope."""
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

    async def test_create_cr_feature_not_found(self, cr_service):
        """Feature not found should raise ValueError."""
        with patch.object(cr_service.feature_repo, "get_by_id", new_callable=AsyncMock, return_value=None):
            with pytest.raises(ValueError, match="not found"):
                await cr_service.create_change_request(uuid.uuid4(), "title", "desc")
