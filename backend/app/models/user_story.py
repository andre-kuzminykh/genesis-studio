"""User Story — describes a user-level behavior within a feature PRD.

Feature: F004 Story Interview Engine
"""
import uuid
from datetime import datetime
import enum

from sqlalchemy import String, Text, DateTime, Boolean, Enum as SAEnum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class UserStoryStatus(str, enum.Enum):
    draft = "draft"
    approved = "approved"
    rejected = "rejected"


class UserStory(Base):
    __tablename__ = "user_stories"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prd_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prd_versions.id"), nullable=False
    )
    story_id: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    benefit: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[UserStoryStatus] = mapped_column(
        SAEnum(UserStoryStatus, name="user_story_status"), default=UserStoryStatus.draft
    )
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    prd_version: Mapped["PRDVersion"] = relationship("PRDVersion", back_populates="user_stories")  # type: ignore[name-defined]  # noqa: F821
