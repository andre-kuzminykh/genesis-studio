"""Git Operation — records of commits and pushes to GitHub.

Feature: F012 GitHub Integration
"""
import uuid
from datetime import datetime
import enum

from sqlalchemy import String, Text, DateTime, Enum as SAEnum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class GitOperationType(str, enum.Enum):
    commit = "commit"
    push = "push"
    read = "read"


class GitOperationStatus(str, enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"


class GitOperation(Base):
    __tablename__ = "git_operations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id: Mapped[uuid.UUID] = mapped_column(
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
        SAEnum(GitOperationStatus, name="git_operation_status"), default=GitOperationStatus.pending
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    repository: Mapped["GitRepository"] = relationship("GitRepository", back_populates="operations")  # type: ignore[name-defined]  # noqa: F821
