"""DeploymentRunModel — tracks a deployment run for a product.

## Трассируемость
Feature: F015 — Local Deployment
"""
from sqlalchemy import DateTime, Text, Enum as SAEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.model.base_model import Base, BaseModel
from backend.app.model.enums import DeploymentTarget, DeploymentStatus

from datetime import datetime


class DeploymentRunModel(Base, BaseModel):
    __tablename__ = "deployment_runs"

    product_id: Mapped["UUID"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False
    )
    target: Mapped[DeploymentTarget] = mapped_column(
        SAEnum(DeploymentTarget, name="deployment_target"), nullable=False
    )
    status: Mapped[DeploymentStatus] = mapped_column(
        SAEnum(DeploymentStatus, name="deployment_status"),
        default=DeploymentStatus.pending,
    )
    logs: Mapped[str | None] = mapped_column(Text, nullable=True)
    endpoints: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    report: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
