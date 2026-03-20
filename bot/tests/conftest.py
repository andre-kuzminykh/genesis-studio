"""Global test fixtures for Genesis Studio bot tests.

## Трассируемость
Feature: P001 — PRD-first платформа

Bot = UI only layer. Tests mock messages and API clients.
"""
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mock_message():
    msg = AsyncMock()
    msg.from_user = MagicMock(id=123, username="testuser")
    msg.text = "Hello"
    msg.answer = AsyncMock()
    return msg


@pytest.fixture
def mock_state():
    state = AsyncMock()
    state.get_data = AsyncMock(return_value={})
    state.set_data = AsyncMock()
    state.update_data = AsyncMock()
    state.clear = AsyncMock()
    state.set_state = AsyncMock()
    return state
