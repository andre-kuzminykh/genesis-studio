"""Pydantic schemas for Product endpoints.

## Трассируемость
Feature: F001 — Product Creation & Discovery
"""
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from backend.app.model.enums import ProductStatus


class ProductCreateSchema(BaseModel):
    idea_text: str = Field(..., min_length=10, description="Product idea in natural language")
    name: str | None = Field(None, max_length=255)
    constraints: dict | None = None


class ProductUpdateSchema(BaseModel):
    name: str | None = None
    summary: str | None = None
    target_users: str | None = None
    goal: str | None = None
    client_type: str | None = None


class ProductResponseSchema(BaseModel):
    id: UUID
    name: str | None
    idea_text: str
    summary: str | None
    target_users: str | None
    goal: str | None
    client_type: str | None
    constraints: dict | None
    status: ProductStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DiscoveryAnswerInputSchema(BaseModel):
    question: str
    answer: str


class DiscoveryResponseSchema(BaseModel):
    product: ProductResponseSchema
    follow_up_questions: list[str]
    is_complete: bool = False
