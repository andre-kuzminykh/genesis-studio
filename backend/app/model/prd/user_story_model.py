"""UserStoryModel — a user story belonging to a PRD version.

## Трассируемость
Feature: F004 — User Stories
"""
from sqlalchemy import Boolean, Enum as SAEnum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base_model import Base, BaseModel
from backend.app.model.enums import UserStoryStatus


class UserStoryModel(Base, BaseModel):
    __tablename__ = "user_stories"

    prd_version_id: Mapped["UUID"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prd_versions.id"), nullable=False
    )
    story_id: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    benefit: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[UserStoryStatus] = mapped_column(
        SAEnum(UserStoryStatus, name="user_story_status"),
        default=UserStoryStatus.draft,
    )
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)

    # --- relationships ---
    prd_version: Mapped["PRDVersionModel"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "PRDVersionModel", back_populates="user_stories"
    )
