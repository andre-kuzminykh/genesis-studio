"""FeatureModel — a specific feature within a product.

## Трассируемость
Feature: F002 — Feature Map Builder
Scenarios: UC-1.2, UC-2.1
"""
from sqlalchemy import String, Text, Integer, Enum as SAEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base_model import Base, BaseModel
from backend.app.model.enums import FeatureStatus


class FeatureModel(Base, BaseModel):
    __tablename__ = "features"

    product_id: Mapped["UUID"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False
    )
    feature_id: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    overview: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[FeatureStatus] = mapped_column(
        SAEnum(FeatureStatus, name="feature_status"), default=FeatureStatus.draft
    )
    interview_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    business_rules: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    product: Mapped["ProductModel"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "ProductModel", back_populates="features"
    )
    prd_versions: Mapped[list["PRDVersionModel"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "PRDVersionModel", back_populates="feature", cascade="all, delete-orphan"
    )
    change_requests: Mapped[list["ChangeRequestModel"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "ChangeRequestModel", back_populates="feature", cascade="all, delete-orphan"
    )
    code_artifacts: Mapped[list["CodeArtifactModel"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "CodeArtifactModel", back_populates="feature", cascade="all, delete-orphan"
    )
