"""UXFlowModel — a UX flow artifact for a PRD version.

## Трассируемость
Feature: F005 — Telegram UX Preview
Feature: F006 — Mermaid Diagrams
"""
from sqlalchemy import Enum as SAEnum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base_model import Base, BaseModel
from backend.app.model.enums import UXFlowType


class UXFlowModel(Base, BaseModel):
    __tablename__ = "ux_flows"

    prd_version_id: Mapped["UUID"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prd_versions.id"), nullable=False
    )
    flow_type: Mapped[UXFlowType] = mapped_column(
        SAEnum(UXFlowType, name="ux_flow_type"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # --- relationships ---
    prd_version: Mapped["PRDVersionModel"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "PRDVersionModel", back_populates="ux_flows"
    )
