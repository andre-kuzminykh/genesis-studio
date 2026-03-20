"""TaskModel — a development task derived from a PRD version.

## Трассируемость
Feature: F003 — PRD Generation
"""
from sqlalchemy import Enum as SAEnum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base_model import Base, BaseModel
from backend.app.model.enums import TaskStatus, TaskType


class TaskModel(Base, BaseModel):
    __tablename__ = "tasks"

    prd_version_id: Mapped["UUID"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prd_versions.id"), nullable=False
    )
    task_id: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    task_type: Mapped[TaskType] = mapped_column(
        SAEnum(TaskType, name="task_type"),
        default=TaskType.backend,
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    dependencies: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus, name="task_status"),
        default=TaskStatus.pending,
    )

    # --- relationships ---
    prd_version: Mapped["PRDVersionModel"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "PRDVersionModel", back_populates="tasks"
    )
