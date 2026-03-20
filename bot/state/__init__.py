"""FSM states for the Genesis Studio bot.

## Трассируемость
Feature: P001 — PRD-first платформа
"""
from aiogram.fsm.state import State, StatesGroup


class ProductCreation(StatesGroup):
    """States for product creation and discovery flow."""
    waiting_for_idea = State()
    answering_discovery = State()
