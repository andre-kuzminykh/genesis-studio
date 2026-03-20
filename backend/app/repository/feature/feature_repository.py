"""FeatureRepository — persistence layer for Feature aggregate.

## Трассируемость
Feature: F002 — Feature Map Builder
"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.repository.base_repository import BaseRepository
from backend.app.model.feature import FeatureModel


class FeatureRepository(BaseRepository[FeatureModel]):
    """Repository for FeatureModel with eager-loading and bulk operations."""

    def __init__(self, session: AsyncSession):
        super().__init__(FeatureModel, session)

    async def get_by_id(self, entity_id: uuid.UUID) -> FeatureModel | None:
        stmt = (
            select(FeatureModel)
            .where(FeatureModel.id == entity_id)
            .options(
                selectinload(FeatureModel.prd_versions),
                selectinload(FeatureModel.change_requests),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_product(self, product_id: uuid.UUID) -> list[FeatureModel]:
        stmt = (
            select(FeatureModel)
            .where(FeatureModel.product_id == product_id)
            .order_by(FeatureModel.sort_order)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, feature: FeatureModel, **kwargs) -> FeatureModel:
        for key, value in kwargs.items():
            if hasattr(feature, key):
                setattr(feature, key, value)
        await self.session.flush()
        return feature

    async def update_status(self, feature: FeatureModel, status) -> FeatureModel:
        feature.status = status
        await self.session.flush()
        return feature

    async def bulk_create(
        self, product_id: uuid.UUID, features_data: list[dict]
    ) -> list[FeatureModel]:
        features: list[FeatureModel] = []
        for data in features_data:
            feature = FeatureModel(product_id=product_id, **data)
            self.session.add(feature)
            features.append(feature)
        await self.session.flush()
        return features
