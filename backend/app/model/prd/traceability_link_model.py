"""TraceabilityLinkModel — a directed link between two traceable artifacts.

## Трассируемость
Feature: F010 — Traceability Matrix
"""
import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.model.base_model import Base, BaseModel


class TraceabilityLinkModel(Base, BaseModel):
    __tablename__ = "traceability_links"

    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )
    target_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )
    link_type: Mapped[str] = mapped_column(String(50), default="derives_from")
    prd_version_id: Mapped["UUID | None"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prd_versions.id"), nullable=True
    )
