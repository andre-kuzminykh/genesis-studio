"""GitOperationModel — records individual git operations (commit, push, read).

## Трассируемость
Feature: F012 — GitHub Integration
"""
from sqlalchemy import String, Text, Enum as SAEnum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base_model import Base, BaseModel
from backend.app.model.enums import GitOperationType, GitOperationStatus


class GitOperationModel(Base, BaseModel):
    __tablename__ = "git_operations"

    repository_id: Mapped["UUID"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("git_repositories.id"), nullable=False
    )
    operation_type: Mapped[GitOperationType] = mapped_column(
        SAEnum(GitOperationType, name="git_operation_type"), nullable=False
    )
    branch: Mapped[str] = mapped_column(String(255), nullable=False)
    commit_sha: Mapped[str | None] = mapped_column(String(40), nullable=True)
    commit_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    files_changed: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[GitOperationStatus] = mapped_column(
        SAEnum(GitOperationStatus, name="git_operation_status"),
        default=GitOperationStatus.pending,
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    repository: Mapped["GitRepositoryModel"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "GitRepositoryModel", back_populates="operations"
    )
