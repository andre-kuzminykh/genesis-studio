"""Integration tests for Product API endpoints.

Feature: F001 Product Creation & Discovery
Scenario: UC-1.1, UC-1.2
"""
import pytest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from backend.app.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestProductAPI:
    """Test product creation and discovery flow."""

    def test_health_endpoint(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_create_product_validation(self, client):
        """FR-1: Validate product creation input."""
        response = client.post("/api/v1/products", json={"idea_text": "short"})
        assert response.status_code == 422  # Validation error for too short text
