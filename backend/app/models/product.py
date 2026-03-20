"""Product entity — top-level object representing a user's product idea.

Feature: F001 Product Creation & Discovery
"""
import uuid
from datetime import datetime

from sqlalchemy import String, Text, DateTime, Enum as SAEnum, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from backend.app.core.database import Base


class ProductStatus(str, enum.Enum):
    draft = "draft"
    discovery_in_progress = "discovery_in_progress"
    feature_map_draft = "feature_map_draft"
    feature_map_approved = "feature_map_approved"
    in_development = "in_development"
    archived = "archived"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    idea_text: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_users: Mapped[str | None] = mapped_column(Text, nullable=True)
    goal: Mapped[str | None] = mapped_column(Text, nullable=True)
    client_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    constraints: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[ProductStatus] = mapped_column(
        SAEnum(ProductStatus, name="product_status"), default=ProductStatus.draft
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    features: Mapped[list["Feature"]] = relationship("Feature", back_populates="product", cascade="all, delete-orphan")  # type: ignore[name-defined]  # noqa: F821
    interview_responses: Mapped[list["InterviewResponse"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "InterviewResponse", back_populates="product", cascade="all, delete-orphan"
    )
    git_repository: Mapped["GitRepository | None"] = relationship("GitRepository", back_populates="product", uselist=False)  # type: ignore[name-defined]  # noqa: F821
