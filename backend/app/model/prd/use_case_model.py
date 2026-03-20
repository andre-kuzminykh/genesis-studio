"""UseCaseModel — a use case (Given/When/Then) for a PRD version.

## Трассируемость
Feature: F007 — Use Cases
"""
from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base_model import Base, BaseModel
from backend.app.model.enums import UseCaseStatus


class UseCaseModel(Base, BaseModel):
    __tablename__ = "use_cases"

    prd_version_id: Mapped["UUID"] = mapped_column(
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
        SAEnum(UseCaseStatus, name="use_case_status"),
        default=UseCaseStatus.draft,
    )
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)

    # --- relationships ---
    prd_version: Mapped["PRDVersionModel"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "PRDVersionModel", back_populates="use_cases"
    )
