"""ProductModel — top-level object representing a user's product idea.

## Трассируемость
Feature: F001 — Product Creation & Discovery
Scenarios: UC-1.1, UC-1.2
"""
from sqlalchemy import String, Text, Enum as SAEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base_model import Base, BaseModel
from backend.app.model.enums import ProductStatus


class ProductModel(Base, BaseModel):
    __tablename__ = "products"

    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    idea_text: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_users: Mapped[str | None] = mapped_column(Text, nullable=True)
    goal: Mapped[str | None] = mapped_column(Text, nullable=True)
    client_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    constraints: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[ProductStatus] = mapped_column(
        SAEnum(ProductStatus, name="product_status"), default=ProductStatus.draft
    )

    features: Mapped[list["FeatureModel"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "FeatureModel", back_populates="product", cascade="all, delete-orphan"
    )
    interview_responses: Mapped[list["InterviewResponseModel"]] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "InterviewResponseModel", back_populates="product", cascade="all, delete-orphan"
    )
    git_repository: Mapped["GitRepositoryModel | None"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "GitRepositoryModel", back_populates="product", uselist=False
    )
