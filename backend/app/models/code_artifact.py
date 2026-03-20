"""Code Artifact — metadata about generated code files.

Feature: F013 Backend Code Generator, F014 Telegram Bot Code Generator
"""
import uuid
from datetime import datetime
import enum

from sqlalchemy import String, Text, DateTime, Enum as SAEnum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class ArtifactType(str, enum.Enum):
    backend = "backend"
    bot = "bot"
    shared = "shared"
    test = "test"
    config = "config"


class CodeArtifact(Base):
    __tablename__ = "code_artifacts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feature_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("features.id"), nullable=False)
    prd_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prd_versions.id"), nullable=False
    )
    artifact_type: Mapped[ArtifactType] = mapped_column(
        SAEnum(ArtifactType, name="artifact_type"), nullable=False
    )
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    feature: Mapped["Feature"] = relationship("Feature", back_populates="code_artifacts")  # type: ignore[name-defined]  # noqa: F821
