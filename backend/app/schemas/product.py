"""Pydantic schemas for Product endpoints."""
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from backend.app.models.product import ProductStatus


class ProductCreate(BaseModel):
    idea_text: str = Field(..., min_length=10, description="Product idea in natural language")
    name: str | None = Field(None, max_length=255)
    constraints: dict | None = None


class ProductUpdate(BaseModel):
    name: str | None = None
    summary: str | None = None
    target_users: str | None = None
    goal: str | None = None
    client_type: str | None = None


class ProductResponse(BaseModel):
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


class DiscoveryAnswerInput(BaseModel):
    question: str
    answer: str


class DiscoveryResponse(BaseModel):
    product: ProductResponse
    follow_up_questions: list[str]
    is_complete: bool = False
