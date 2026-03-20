"""TestCaseModel — a test case linked to a PRD version.

## Трассируемость
Feature: F009 — Test Cases
"""
from sqlalchemy import Enum as SAEnum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base_model import Base, BaseModel
from backend.app.model.enums import TestCaseStatus, TestCaseType


class TestCaseModel(Base, BaseModel):
    __tablename__ = "test_cases"

    prd_version_id: Mapped["UUID"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prd_versions.id"), nullable=False
    )
    test_id: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    test_type: Mapped[TestCaseType] = mapped_column(
        SAEnum(TestCaseType, name="test_case_type"),
        default=TestCaseType.unit,
    )
    preconditions: Mapped[str | None] = mapped_column(Text, nullable=True)
    steps: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    expected_result: Mapped[str] = mapped_column(Text, nullable=False)
    scenario_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[TestCaseStatus] = mapped_column(
        SAEnum(TestCaseStatus, name="test_case_status"),
        default=TestCaseStatus.draft,
    )

    # --- relationships ---
    prd_version: Mapped["PRDVersionModel"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "PRDVersionModel", back_populates="test_cases"
    )
