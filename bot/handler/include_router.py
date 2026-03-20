"""Router inclusion — connects all widget routers to the dispatcher.

## Трассируемость
Feature: P001 — PRD-first платформа
"""
from aiogram import Dispatcher

from bot.handler.v1.user.product.F001.start_widget import router as start_router
from bot.handler.v1.user.product.F001.create_product_widget import router as create_product_router
from bot.handler.v1.user.feature.F002.feature_actions_widget import router as feature_actions_router


def register_routers(dp: Dispatcher) -> None:
    dp.include_router(start_router)
    dp.include_router(create_product_router)
    dp.include_router(feature_actions_router)
