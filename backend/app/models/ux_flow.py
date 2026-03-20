"""UX Flow — Telegram UI preview and Mermaid diagrams for a feature.

Feature: F005 Telegram UX Preview, F006 Mermaid Flow Generator
"""
import uuid
from datetime import datetime
import enum

from sqlalchemy import String, Text, DateTime, Enum as SAEnum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class UXFlowType(str, enum.Enum):
    telegram_preview = "telegram_preview"
    mermaid_user_flow = "mermaid_user_flow"
    mermaid_sequence = "mermaid_sequence"
    mermaid_state = "mermaid_state"


class UXFlow(Base):
    __tablename__ = "ux_flows"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prd_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prd_versions.id"), nullable=False
    )
    flow_type: Mapped[UXFlowType] = mapped_column(SAEnum(UXFlowType, name="ux_flow_type"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    prd_version: Mapped["PRDVersion"] = relationship("PRDVersion", back_populates="ux_flows")  # type: ignore[name-defined]  # noqa: F821
