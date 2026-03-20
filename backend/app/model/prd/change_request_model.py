"""ChangeRequestModel — a change request against a feature's PRD.

## Трассируемость
Feature: F011 — Change Requests
"""
from datetime import datetime

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base_model import Base, BaseModel
from backend.app.model.enums import ChangeRequestStatus


class ChangeRequestModel(Base, BaseModel):
    __tablename__ = "change_requests"

    feature_id: Mapped["UUID"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("features.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    impact_analysis: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    diff_summary: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[ChangeRequestStatus] = mapped_column(
        SAEnum(ChangeRequestStatus, name="change_request_status"),
        default=ChangeRequestStatus.pending,
    )
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # --- relationships ---
    feature: Mapped["FeatureModel"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "FeatureModel", back_populates="change_requests"
    )
    prd_version: Mapped["PRDVersionModel | None"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "PRDVersionModel", back_populates="change_request", uselist=False
    )
