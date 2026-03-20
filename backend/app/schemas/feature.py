"""Pydantic schemas for Feature endpoints."""
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from backend.app.models.feature import FeatureStatus


class FeatureCreate(BaseModel):
    feature_id: str = Field(..., max_length=50)
    name: str = Field(..., max_length=255)
    overview: str | None = None
    sort_order: int = 0


class FeatureUpdate(BaseModel):
    name: str | None = None
    overview: str | None = None
    sort_order: int | None = None


class FeatureResponse(BaseModel):
    id: UUID
    product_id: UUID
    feature_id: str
    name: str
    overview: str | None
    sort_order: int
    status: FeatureStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class FeatureMapApproval(BaseModel):
    feature_ids: list[UUID]


class FeatureMapResponse(BaseModel):
    product_id: UUID
    features: list[FeatureResponse]
    is_approved: bool
