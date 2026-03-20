"""Fixtures for F003 — Feature PRD Generator tests.

## Трассируемость
Feature: F003 — Feature PRD Generator
"""
import uuid
from unittest.mock import MagicMock

import pytest

from backend.app.service.feature.prd_service import PRDService


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
