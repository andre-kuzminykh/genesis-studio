"""GitRepositoryModel — links a product to its GitHub repository.

## Трассируемость
Feature: F012 — GitHub Integration
Scenarios: UC-4.1
"""
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base_model import Base, BaseModel


class GitRepositoryModel(Base, BaseModel):
    __tablename__ = "git_repositories"

    product_id: Mapped["UUID"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), unique=True, nullable=False
    )
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    repo_name: Mapped[str] = mapped_column(String(255), nullable=False)
    default_branch: Mapped[str] = mapped_column(String(100), default="main")
    github_url: Mapped[str] = mapped_column(String(500), nullable=False)

    product: Mapped["ProductModel"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "ProductModel", back_populates="git_repository"
    )
    operations: Mapped[list["GitOperationModel"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "GitOperationModel", back_populates="repository", cascade="all, delete-orphan"
    )
