"""CodeArtifactModel — generated code file linked to a feature and PRD version.

## Трассируемость
Feature: F013 — Code Generation, F014 — Code Artifact Management
"""
from sqlalchemy import String, Text, Enum as SAEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base_model import Base, BaseModel
from backend.app.model.enums import ArtifactType


class CodeArtifactModel(Base, BaseModel):
    __tablename__ = "code_artifacts"

    feature_id: Mapped["UUID"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("features.id"), nullable=False
    )
    prd_version_id: Mapped["UUID"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prd_versions.id"), nullable=False
    )
    artifact_type: Mapped[ArtifactType] = mapped_column(
        SAEnum(ArtifactType, name="artifact_type"), nullable=False
    )
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    feature: Mapped["FeatureModel"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "FeatureModel", back_populates="code_artifacts"
    )
