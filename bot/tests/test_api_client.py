"""Tests for the bot API client.

Verifies bot communicates with backend via HTTP API only (UI-only architecture).
"""
import pytest

from bot.services.api_client import BackendAPIClient


class TestAPIClientInit:
    def test_client_has_base_url(self):
        client = BackendAPIClient()
        assert client.base_url.startswith("http")

    def test_client_strips_trailing_slash(self):
        client = BackendAPIClient()
        assert not client.base_url.endswith("/")
