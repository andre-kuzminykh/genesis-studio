"""Fixtures for F013 — Backend Code Generator tests.

## Трассируемость
Feature: F013 — Backend Code Generator
"""
import pytest

from backend.app.service.feature.codegen_service import CodegenService


@pytest.fixture
def codegen_service(mock_session):
    return CodegenService(mock_session)
