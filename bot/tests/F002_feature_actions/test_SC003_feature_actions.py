"""Тест SC003 — Feature action buttons.

## Трассируемость
Feature: F002 — Feature Actions
Scenario: SC003 — User taps action button to progress through PRD workflow

## BDD
Given: User is viewing a feature
When:  User taps an action button
Then:  Bot calls backend API and shows result
"""
import pytest

from bot.service.api.features_api import FeaturesAPI


class TestFeaturesAPIClient:
    """Tests that features API client is correctly configured."""

    def test_client_has_base_url(self):
        client = FeaturesAPI()
        assert client.base_url.startswith("http")
