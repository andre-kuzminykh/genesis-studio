"""Router inclusion — connects all endpoint routers to the app.

## Трассируемость
Feature: P001 — PRD-first платформа
"""
from fastapi import FastAPI

from backend.app.api.v1.endpoints import products_router, features_router, github_router

API_V1_PREFIX = "/api/v1"


def include_routers(application: FastAPI) -> None:
    application.include_router(products_router, prefix=API_V1_PREFIX)
    application.include_router(features_router, prefix=API_V1_PREFIX)
    application.include_router(github_router, prefix=API_V1_PREFIX)
