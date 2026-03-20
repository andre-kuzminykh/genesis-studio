"""Unit tests for PRDService.

Feature: F003 Feature PRD Generator, F007 Use Case Generator,
F008 Requirements Derivation, F009 Test Generator
Scenario: UC-2.1, UC-2.2, UC-3.1
"""
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.app.services.prd_service import PRDService


@pytest.fixture
def prd_service(mock_session):
    return PRDService(mock_session)


@pytest.fixture
def mock_feature():
    f = MagicMock()
    f.id = uuid.uuid4()
    f.feature_id = "F001"
    f.name = "Test Feature"
    f.overview = "Test overview"
    f.product_id = uuid.uuid4()
    return f


@pytest.fixture
def mock_prd_version():
    prd = MagicMock()
    prd.id = uuid.uuid4()
    prd.version_number = 1
    prd.content = {"feature_id": "F001"}
    prd.use_cases = []
    prd.requirements = []
    prd.test_cases = []
    prd.tasks = []
    prd.user_stories = []
    prd.ux_flows = []
    return prd


class TestGeneratePRDDraft:
    """Tests for UC-2.1 — PRD draft generation."""

    async def test_generate_prd_draft_creates_version(self, prd_service, mock_feature):
        """FR-7: Generate feature-level PRD in canonical format."""
        mock_prd = MagicMock()
        mock_prd.id = uuid.uuid4()
        mock_prd.version_number = 1

        with patch.object(prd_service.feature_repo, "get_by_id", new_callable=AsyncMock, return_value=mock_feature):
            with patch.object(prd_service.prd_repo, "create_prd_version", new_callable=AsyncMock, return_value=mock_prd):
                with patch.object(prd_service.prd_repo, "bulk_create_stories", new_callable=AsyncMock, return_value=[]):
                    with patch.object(prd_service.feature_repo, "update_status", new_callable=AsyncMock):
                        result = await prd_service.generate_prd_draft(mock_feature.id)

        assert "prd_version" in result
        assert "user_stories" in result

    async def test_generate_prd_draft_feature_not_found(self, prd_service):
        """Feature not found should raise ValueError."""
        with patch.object(prd_service.feature_repo, "get_by_id", new_callable=AsyncMock, return_value=None):
            with pytest.raises(ValueError, match="not found"):
                await prd_service.generate_prd_draft(uuid.uuid4())


class TestTraceability:
    """Tests for F010 — Traceability Graph."""

    async def test_get_traceability_returns_counts(self, prd_service, mock_prd_version):
        """NFR-10: All requirements and tests must have traceable links."""
        with patch.object(prd_service.prd_repo, "get_current_prd_version", new_callable=AsyncMock, return_value=mock_prd_version):
            with patch.object(prd_service.prd_repo, "get_links_for_prd", new_callable=AsyncMock, return_value=[]):
                result = await prd_service.get_traceability(uuid.uuid4())

        assert "user_stories_count" in result
        assert "use_cases_count" in result
        assert "requirements_count" in result
        assert "test_cases_count" in result
        assert "links" in result
