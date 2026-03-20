"""Exception handlers for the API.

## Трассируемость
Feature: P001 — PRD-first платформа
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.app.core.exceptions import AppException


def register_exception_handlers(application: FastAPI) -> None:
    @application.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )
