"""FastAPI application entry point for Genesis Studio backend.

## Трассируемость
Feature: P001 — PRD-first платформа

## Бизнес-контекст
Точка входа backend-сервиса. Подключает все роутеры и обработчики ошибок.
"""
from backend.app.core.loader import app
from backend.app.api.v1.include_router import include_routers
from backend.app.api.v1.exception_handlers import register_exception_handlers

# Ensure all models are imported for Alembic
import backend.app.model  # noqa: F401

include_routers(app)
register_exception_handlers(app)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "genesis-studio-backend"}
