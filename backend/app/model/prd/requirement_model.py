"""RequirementModel — a functional or non-functional requirement.

## Трассируемость
Feature: F008 — Requirements
"""
from sqlalchemy import Enum as SAEnum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base_model import Base, BaseModel
from backend.app.model.enums import RequirementType


class RequirementModel(Base, BaseModel):
    __tablename__ = "requirements"

    prd_version_id: Mapped["UUID"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prd_versions.id"), nullable=False
    )
    req_id: Mapped[str] = mapped_column(String(50), nullable=False)
    req_type: Mapped[RequirementType] = mapped_column(
        SAEnum(RequirementType, name="requirement_type"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    # --- relationships ---
    prd_version: Mapped["PRDVersionModel"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "PRDVersionModel", back_populates="requirements"
    )
