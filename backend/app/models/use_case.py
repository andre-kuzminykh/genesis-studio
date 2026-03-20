"""Use Case — BDD-style scenario derived from user stories.

Feature: F007 Use Case Generator
"""
import uuid
from datetime import datetime
import enum

from sqlalchemy import String, Text, DateTime, Boolean, Enum as SAEnum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class UseCaseStatus(str, enum.Enum):
    draft = "draft"
    approved = "approved"


class UseCase(Base):
    __tablename__ = "use_cases"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prd_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prd_versions.id"), nullable=False
    )
    use_case_id: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    given: Mapped[str] = mapped_column(Text, nullable=False)
    when: Mapped[str] = mapped_column(Text, nullable=False)
    then: Mapped[str] = mapped_column(Text, nullable=False)
    input_spec: Mapped[str | None] = mapped_column(Text, nullable=True)
    output_spec: Mapped[str | None] = mapped_column(Text, nullable=True)
    state_transition: Mapped[str | None] = mapped_column(Text, nullable=True)
    edge_cases: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[UseCaseStatus] = mapped_column(
        SAEnum(UseCaseStatus, name="use_case_status"), default=UseCaseStatus.draft
    )
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    prd_version: Mapped["PRDVersion"] = relationship("PRDVersion", back_populates="use_cases")  # type: ignore[name-defined]  # noqa: F821
