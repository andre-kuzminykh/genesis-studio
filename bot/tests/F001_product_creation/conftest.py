"""Fixtures for F001 — Product Creation bot tests.

## Трассируемость
Feature: F001 — Product Creation & Discovery
"""
import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_callback():
    cb = AsyncMock()
    cb.from_user = MagicMock(id=123, username="testuser")
    cb.data = "test_action:123"
    cb.answer = AsyncMock()
    cb.message = AsyncMock()
    cb.message.answer = AsyncMock()
    return cb
