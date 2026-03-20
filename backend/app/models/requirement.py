"""Requirement — functional and non-functional requirements derived from use cases.

Feature: F008 Requirements Derivation
"""
import uuid
from datetime import datetime
import enum

from sqlalchemy import String, Text, DateTime, Enum as SAEnum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class RequirementType(str, enum.Enum):
    functional = "functional"
    non_functional = "non_functional"


class Requirement(Base):
    __tablename__ = "requirements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prd_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prd_versions.id"), nullable=False
    )
    req_id: Mapped[str] = mapped_column(String(50), nullable=False)
    req_type: Mapped[RequirementType] = mapped_column(
        SAEnum(RequirementType, name="requirement_type"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    prd_version: Mapped["PRDVersion"] = relationship("PRDVersion", back_populates="requirements")  # type: ignore[name-defined]  # noqa: F821
