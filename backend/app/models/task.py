"""Task — implementation tasks derived from requirements and tests.

Feature: F003 Feature PRD Generator
"""
import uuid
from datetime import datetime
import enum

from sqlalchemy import String, Text, DateTime, Integer, Enum as SAEnum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskType(str, enum.Enum):
    backend = "backend"
    bot = "bot"
    shared = "shared"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prd_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prd_versions.id"), nullable=False
    )
    task_id: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    task_type: Mapped[TaskType] = mapped_column(SAEnum(TaskType, name="task_type"), default=TaskType.backend)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    dependencies: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus, name="task_status"), default=TaskStatus.pending
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    prd_version: Mapped["PRDVersion"] = relationship("PRDVersion", back_populates="tasks")  # type: ignore[name-defined]  # noqa: F821
