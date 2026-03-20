"""FastAPI application factory.

## Трассируемость
Feature: P001 — PRD-first платформа
"""
from fastapi import FastAPI

from backend.app.core.config import settings


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        description="PRD-first platform for bot/backend generation and GitHub delivery",
        version="0.1.0",
    )
    return application


app = create_app()
