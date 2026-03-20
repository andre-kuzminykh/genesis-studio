"""Application exceptions with user-level error messages.

## Трассируемость
Feature: P001 — PRD-first платформа
"""


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppException):
    """Entity not found (404)."""

    def __init__(self, entity: str, entity_id: str | None = None):
        detail = f"{entity} not found" if not entity_id else f"{entity} {entity_id} not found"
        super().__init__(detail, status_code=404)


class ValidationError(AppException):
    """Input validation failed (422)."""

    def __init__(self, message: str):
        super().__init__(message, status_code=422)


class StateConflictError(AppException):
    """Operation conflicts with current state (409)."""

    def __init__(self, message: str):
        super().__init__(message, status_code=409)


class ExternalServiceError(AppException):
    """External service unavailable or failed (502/503)."""

    def __init__(self, service: str, message: str):
        super().__init__(f"{service}: {message}", status_code=502)
