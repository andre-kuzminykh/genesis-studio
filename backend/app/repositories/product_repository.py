"""Repository layer for Product and InterviewResponse persistence.

Feature: F001 Product Creation & Discovery
"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.models.product import Product, ProductStatus
from backend.app.models.interview_response import InterviewResponse


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, idea_text: str, name: str | None = None, constraints: dict | None = None) -> Product:
        product = Product(idea_text=idea_text, name=name, constraints=constraints, status=ProductStatus.draft)
        self.session.add(product)
        await self.session.flush()
        return product

    async def get_by_id(self, product_id: uuid.UUID) -> Product | None:
        stmt = (
            select(Product)
            .options(selectinload(Product.features), selectinload(Product.interview_responses))
            .where(Product.id == product_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_all(self) -> list[Product]:
        stmt = select(Product).order_by(Product.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_status(self, product: Product, status: ProductStatus) -> Product:
        product.status = status
        await self.session.flush()
        return product

    async def update(self, product: Product, **kwargs) -> Product:
        for key, value in kwargs.items():
            if hasattr(product, key) and value is not None:
                setattr(product, key, value)
        await self.session.flush()
        return product

    async def add_interview_response(
        self, product_id: uuid.UUID, question: str, answer: str, step_number: int
    ) -> InterviewResponse:
        response = InterviewResponse(
            product_id=product_id, question=question, answer=answer, step_number=step_number
        )
        self.session.add(response)
        await self.session.flush()
        return response
