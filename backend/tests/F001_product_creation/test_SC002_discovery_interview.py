"""Тест SC002 — Discovery interview flow.

## Трассируемость
Feature: F001 — Product Creation & Discovery
Scenario: SC002 — User answers discovery questions

## BDD
Given: Product exists in discovery_in_progress state
When:  User submits answer to current question
Then:  System stores answer and returns next questions or marks discovery complete
"""
import pytest

from backend.app.service.product.discovery_service import DISCOVERY_QUESTIONS


def test_discovery_questions_are_defined():
    """
    Given: Discovery service is configured
    When:  Checking discovery questions
    Then:  At least 3 well-formed questions exist
    """
    assert len(DISCOVERY_QUESTIONS) >= 3
    for q in DISCOVERY_QUESTIONS:
        assert isinstance(q, str)
        assert len(q) > 10
