"""Test Case — generated from use cases and acceptance criteria.

Feature: F009 Test Generator
"""
import uuid
from datetime import datetime
import enum

from sqlalchemy import String, Text, DateTime, Enum as SAEnum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class TestCaseType(str, enum.Enum):
    unit = "unit"
    integration = "integration"
    e2e = "e2e"
    acceptance = "acceptance"


class TestCaseStatus(str, enum.Enum):
    draft = "draft"
    approved = "approved"


class TestCase(Base):
    __tablename__ = "test_cases"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prd_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prd_versions.id"), nullable=False
    )
    test_id: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    test_type: Mapped[TestCaseType] = mapped_column(
        SAEnum(TestCaseType, name="test_case_type"), default=TestCaseType.unit
    )
    preconditions: Mapped[str | None] = mapped_column(Text, nullable=True)
    steps: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    expected_result: Mapped[str] = mapped_column(Text, nullable=False)
    scenario_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[TestCaseStatus] = mapped_column(
        SAEnum(TestCaseStatus, name="test_case_status"), default=TestCaseStatus.draft
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    prd_version: Mapped["PRDVersion"] = relationship("PRDVersion", back_populates="test_cases")  # type: ignore[name-defined]  # noqa: F821
