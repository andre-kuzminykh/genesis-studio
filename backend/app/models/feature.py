"""Feature entity — a specific feature within a product.

Feature: F002 Feature Map Builder
"""
import uuid
from datetime import datetime
import enum

from sqlalchemy import String, Text, Integer, DateTime, Enum as SAEnum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class FeatureStatus(str, enum.Enum):
    draft = "draft"
    feature_selected = "feature_selected"
    prd_draft_created = "prd_draft_created"
    stories_approved = "stories_approved"
    ux_approved = "ux_approved"
    use_cases_approved = "use_cases_approved"
    requirements_generated = "requirements_generated"
    tests_generated = "tests_generated"
    tests_approved = "tests_approved"
    code_generated = "code_generated"
    pushed_to_github = "pushed_to_github"
    deployed_local = "deployed_local"
    deploy_failed = "deploy_failed"


class Feature(Base):
    __tablename__ = "features"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    feature_id: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    overview: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[FeatureStatus] = mapped_column(
        SAEnum(FeatureStatus, name="feature_status"), default=FeatureStatus.draft
    )
    interview_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    business_rules: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="features")  # type: ignore[name-defined]  # noqa: F821
    prd_versions: Mapped[list["PRDVersion"]] = relationship("PRDVersion", back_populates="feature", cascade="all, delete-orphan")  # type: ignore[name-defined]  # noqa: F821
    change_requests: Mapped[list["ChangeRequest"]] = relationship("ChangeRequest", back_populates="feature", cascade="all, delete-orphan")  # type: ignore[name-defined]  # noqa: F821
    code_artifacts: Mapped[list["CodeArtifact"]] = relationship("CodeArtifact", back_populates="feature", cascade="all, delete-orphan")  # type: ignore[name-defined]  # noqa: F821
