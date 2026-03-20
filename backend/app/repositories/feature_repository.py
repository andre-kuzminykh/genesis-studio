"""Repository layer for Feature persistence.

Feature: F002 Feature Map Builder
"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.models.feature import Feature, FeatureStatus


class FeatureRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, product_id: uuid.UUID, feature_id: str, name: str, overview: str | None = None, sort_order: int = 0) -> Feature:
        feature = Feature(
            product_id=product_id, feature_id=feature_id, name=name, overview=overview, sort_order=sort_order
        )
        self.session.add(feature)
        await self.session.flush()
        return feature

    async def get_by_id(self, fid: uuid.UUID) -> Feature | None:
        stmt = (
            select(Feature)
            .options(selectinload(Feature.prd_versions), selectinload(Feature.change_requests))
            .where(Feature.id == fid)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_product(self, product_id: uuid.UUID) -> list[Feature]:
        stmt = select(Feature).where(Feature.product_id == product_id).order_by(Feature.sort_order)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, feature: Feature, **kwargs) -> Feature:
        for key, value in kwargs.items():
            if hasattr(feature, key) and value is not None:
                setattr(feature, key, value)
        await self.session.flush()
        return feature

    async def update_status(self, feature: Feature, status: FeatureStatus) -> Feature:
        feature.status = status
        await self.session.flush()
        return feature

    async def delete(self, feature: Feature) -> None:
        await self.session.delete(feature)
        await self.session.flush()

    async def bulk_create(self, product_id: uuid.UUID, features_data: list[dict]) -> list[Feature]:
        features = []
        for i, fd in enumerate(features_data):
            feature = Feature(
                product_id=product_id,
                feature_id=fd.get("feature_id", f"F{i+1:03d}"),
                name=fd["name"],
                overview=fd.get("overview"),
                sort_order=fd.get("sort_order", i),
            )
            self.session.add(feature)
            features.append(feature)
        await self.session.flush()
        return features
