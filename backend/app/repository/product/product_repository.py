"""ProductRepository — persistence layer for Product aggregate.

## Трассируемость
Feature: F001 — Product Creation & Discovery
Scenarios: UC-1.1, UC-1.2
"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.repository.base_repository import BaseRepository
from backend.app.model.product import ProductModel, InterviewResponseModel


class ProductRepository(BaseRepository[ProductModel]):
    """Repository for ProductModel with eager-loading and status helpers."""

    def __init__(self, session: AsyncSession):
        super().__init__(ProductModel, session)

    async def get_by_id(self, entity_id: uuid.UUID) -> ProductModel | None:
        stmt = (
            select(ProductModel)
            .where(ProductModel.id == entity_id)
            .options(
                selectinload(ProductModel.features),
                selectinload(ProductModel.interview_responses),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> list[ProductModel]:
        stmt = select(ProductModel).order_by(ProductModel.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_status(self, product: ProductModel, status) -> ProductModel:
        product.status = status
        await self.session.flush()
        return product

    async def update(self, product: ProductModel, **kwargs) -> ProductModel:
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        await self.session.flush()
        return product

    async def add_interview_response(
        self,
        product_id: uuid.UUID,
        question: str,
        answer: str,
        step_number: int,
    ) -> InterviewResponseModel:
        response = InterviewResponseModel(
            product_id=product_id,
            question=question,
            answer=answer,
            step_number=step_number,
        )
        self.session.add(response)
        await self.session.flush()
        return response
