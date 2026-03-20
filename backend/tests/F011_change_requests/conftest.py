"""Fixtures for F011 — PRD Versioning & Change Requests tests.

## Трассируемость
Feature: F011 — PRD Versioning & Change Requests
"""
import uuid
from unittest.mock import MagicMock

import pytest

from backend.app.service.feature.change_request_service import ChangeRequestService


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
