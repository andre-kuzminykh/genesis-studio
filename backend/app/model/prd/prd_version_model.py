"""PRDVersionModel — a versioned snapshot of a PRD for a feature.

## Трассируемость
Feature: F003 — PRD Generation
Scenarios: UC-2.1, UC-2.2, UC-3.1
"""
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum as SAEnum, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base_model import Base, BaseModel
from backend.app.model.enums import PRDVersionStatus


class PRDVersionModel(Base, BaseModel):
    __tablename__ = "prd_versions"

    feature_id: Mapped["UUID"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("features.id"), nullable=False
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[dict] = mapped_column(JSONB, nullable=False)
    acceptance_criteria: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[PRDVersionStatus] = mapped_column(
        SAEnum(PRDVersionStatus, name="prd_version_status"),
        default=PRDVersionStatus.draft,
    )
    is_current: Mapped[bool] = mapped_column(Boolean, default=True)
    change_request_id: Mapped["UUID | None"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("change_requests.id"), nullable=True
    )
    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # --- relationships ---
    feature: Mapped["FeatureModel"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "FeatureModel", back_populates="prd_versions"
    )
    change_request: Mapped["ChangeRequestModel | None"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "ChangeRequestModel", back_populates="prd_version"
    )
    user_stories: Mapped[list["UserStoryModel"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "UserStoryModel", back_populates="prd_version", cascade="all, delete-orphan"
    )
    ux_flows: Mapped[list["UXFlowModel"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "UXFlowModel", back_populates="prd_version", cascade="all, delete-orphan"
    )
    use_cases: Mapped[list["UseCaseModel"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "UseCaseModel", back_populates="prd_version", cascade="all, delete-orphan"
    )
    requirements: Mapped[list["RequirementModel"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "RequirementModel", back_populates="prd_version", cascade="all, delete-orphan"
    )
    test_cases: Mapped[list["TestCaseModel"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "TestCaseModel", back_populates="prd_version", cascade="all, delete-orphan"
    )
    tasks: Mapped[list["TaskModel"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "TaskModel", back_populates="prd_version", cascade="all, delete-orphan"
    )
