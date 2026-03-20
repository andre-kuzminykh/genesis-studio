"""Fixtures for F001 — Product Creation & Discovery tests.

## Трассируемость
Feature: F001 — Product Creation & Discovery
"""
import pytest
from unittest.mock import AsyncMock

from backend.app.service.product.discovery_service import DiscoveryService


@pytest.fixture
def discovery_service(mock_session):
    return DiscoveryService(mock_session)
