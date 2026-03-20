"""InterviewResponseModel — stores discovery interview Q&A pairs.

## Трассируемость
Feature: F001 — Product Creation & Discovery
Scenarios: UC-1.1
"""
from sqlalchemy import Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.model.base_model import Base, BaseModel


class InterviewResponseModel(Base, BaseModel):
    __tablename__ = "interview_responses"

    product_id: Mapped["UUID"] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False
    )
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    step_number: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    product: Mapped["ProductModel"] = relationship(  # type: ignore[name-defined]  # noqa: F821
        "ProductModel", back_populates="interview_responses"
    )
