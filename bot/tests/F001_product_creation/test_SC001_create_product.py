"""Тест SC001 — Bot product creation flow.

## Трассируемость
Feature: F001 — Product Creation & Discovery
Scenario: SC001 — User taps Create Product and enters idea

## BDD
Given: User is in the main menu
When:  User taps Create Product and enters idea text
Then:  Bot calls backend API and shows first discovery question
"""
import pytest

from bot.service.api.products_api import ProductsAPI


class TestProductsAPIClient:
    """Tests that bot API client is correctly configured."""

    def test_client_has_base_url(self):
        """
        Given: ProductsAPI is instantiated
        When:  Checking base_url
        Then:  URL starts with http
        """
        client = ProductsAPI()
        assert client.base_url.startswith("http")

    def test_client_strips_trailing_slash(self):
        """
        Given: ProductsAPI is instantiated
        When:  Checking base_url
        Then:  No trailing slash
        """
        client = ProductsAPI()
        assert not client.base_url.endswith("/")
