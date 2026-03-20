"""PRD Version — immutable snapshot of a feature-level PRD.

Feature: F003 Feature PRD Generator, F011 PRD Versioning & Change Requests
"""
import uuid
from datetime import datetime
import enum

from sqlalchemy import Integer, Text, DateTime, Boolean, Enum as SAEnum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class PRDVersionStatus(str, enum.Enum):
    draft = "draft"
    approved = "approved"
    superseded = "superseded"


class PRDVersion(Base):
    __tablename__ = "prd_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feature_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("features.id"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    content: Mapped[dict] = mapped_column(JSONB, nullable=False)
    acceptance_criteria: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[PRDVersionStatus] = mapped_column(
        SAEnum(PRDVersionStatus, name="prd_version_status"), default=PRDVersionStatus.draft
    )
    is_current: Mapped[bool] = mapped_column(Boolean, default=True)
    change_request_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("change_requests.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    feature: Mapped["Feature"] = relationship("Feature", back_populates="prd_versions")  # type: ignore[name-defined]  # noqa: F821
    change_request: Mapped["ChangeRequest | None"] = relationship("ChangeRequest", back_populates="prd_version")  # type: ignore[name-defined]  # noqa: F821
    user_stories: Mapped[list["UserStory"]] = relationship("UserStory", back_populates="prd_version", cascade="all, delete-orphan")  # type: ignore[name-defined]  # noqa: F821
    ux_flows: Mapped[list["UXFlow"]] = relationship("UXFlow", back_populates="prd_version", cascade="all, delete-orphan")  # type: ignore[name-defined]  # noqa: F821
    use_cases: Mapped[list["UseCase"]] = relationship("UseCase", back_populates="prd_version", cascade="all, delete-orphan")  # type: ignore[name-defined]  # noqa: F821
    requirements: Mapped[list["Requirement"]] = relationship("Requirement", back_populates="prd_version", cascade="all, delete-orphan")  # type: ignore[name-defined]  # noqa: F821
    test_cases: Mapped[list["TestCase"]] = relationship("TestCase", back_populates="prd_version", cascade="all, delete-orphan")  # type: ignore[name-defined]  # noqa: F821
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="prd_version", cascade="all, delete-orphan")  # type: ignore[name-defined]  # noqa: F821
