"""Global test configuration and fixtures for Genesis Studio backend tests.

## Трассируемость
Feature: P001 — PRD-first платформа
"""
import uuid
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def mock_session():
    """Create a mock async session for unit tests."""
    session = AsyncMock(spec=AsyncSession)
    session.flush = AsyncMock()
    session.commit = AsyncMock()
    session.execute = AsyncMock()
    session.add = AsyncMock()
    session.delete = AsyncMock()
    return session


@pytest.fixture
def sample_product_id():
    return uuid.uuid4()


@pytest.fixture
def sample_feature_id():
    return uuid.uuid4()


@pytest.fixture
def sample_idea_text():
    return "A Telegram bot that helps users track their fitness goals and provides daily workout recommendations"
