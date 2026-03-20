"""Change Request — tracks changes to a feature and triggers new PRD versions.

Feature: F011 PRD Versioning & Change Requests
"""
import uuid
from datetime import datetime
import enum

from sqlalchemy import String, Text, DateTime, Enum as SAEnum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class ChangeRequestStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    applied = "applied"


class ChangeRequest(Base):
    __tablename__ = "change_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feature_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("features.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    impact_analysis: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    diff_summary: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[ChangeRequestStatus] = mapped_column(
        SAEnum(ChangeRequestStatus, name="change_request_status"), default=ChangeRequestStatus.pending
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    feature: Mapped["Feature"] = relationship("Feature", back_populates="change_requests")  # type: ignore[name-defined]  # noqa: F821
    prd_version: Mapped["PRDVersion | None"] = relationship("PRDVersion", back_populates="change_request", uselist=False)  # type: ignore[name-defined]  # noqa: F821
