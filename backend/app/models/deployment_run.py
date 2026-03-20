"""Deployment Run — records of local deployment attempts.

Feature: F015 Local Deployment Orchestrator
"""
import uuid
from datetime import datetime
import enum

from sqlalchemy import String, Text, DateTime, Enum as SAEnum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class DeploymentStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    success = "success"
    failed = "failed"


class DeploymentTarget(str, enum.Enum):
    backend = "backend"
    bot = "bot"
    both = "both"


class DeploymentRun(Base):
    __tablename__ = "deployment_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    target: Mapped[DeploymentTarget] = mapped_column(
        SAEnum(DeploymentTarget, name="deployment_target"), nullable=False
    )
    status: Mapped[DeploymentStatus] = mapped_column(
        SAEnum(DeploymentStatus, name="deployment_status"), default=DeploymentStatus.pending
    )
    logs: Mapped[str | None] = mapped_column(Text, nullable=True)
    endpoints: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    report: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
