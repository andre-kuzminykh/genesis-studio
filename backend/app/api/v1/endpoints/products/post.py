"""Product POST endpoints — creation, discovery, feature map.

## Трассируемость
Feature: F001 Product Creation & Discovery, F002 Feature Map Builder
Scenarios: UC-1.1, UC-1.2
"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_session
from backend.app.schema.product import (
    ProductCreateSchema,
    DiscoveryAnswerInputSchema,
    DiscoveryResponseSchema,
    ProductResponseSchema,
)
from backend.app.schema.feature import (
    FeatureResponseSchema,
    FeatureMapApprovalSchema,
    FeatureMapResponseSchema,
)
from backend.app.service.product import DiscoveryService

router = APIRouter()


@router.post("/", response_model=DiscoveryResponseSchema, status_code=201)
async def create_product(data: ProductCreateSchema, session: AsyncSession = Depends(get_session)):
    """Create a new product from a text idea and start discovery.

    ## Трассируемость
    Feature: F001 Product Creation & Discovery
    Scenarios: UC-1.1

    FR-1: Create product from text description.
    FR-2: Extract product summary, target users, goal, client type, initial feature map.
    """
    service = DiscoveryService(session)
    result = await service.create_product(data.idea_text, data.name, data.constraints)
    return DiscoveryResponseSchema(
        product=ProductResponseSchema.model_validate(result["product"]),
        follow_up_questions=result["follow_up_questions"],
        is_complete=result["is_complete"],
    )


@router.post("/{product_id}/discovery", response_model=DiscoveryResponseSchema)
async def submit_discovery(
    product_id: UUID, data: DiscoveryAnswerInputSchema, session: AsyncSession = Depends(get_session)
):
    """Submit a discovery answer and get follow-up questions.

    ## Трассируемость
    Feature: F001 Product Creation & Discovery
    Scenarios: UC-1.1

    FR-3: Save all discovery inputs in linked data model.
    """
    service = DiscoveryService(session)
    try:
        result = await service.submit_discovery_answer(product_id, data.question, data.answer)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return DiscoveryResponseSchema(
        product=ProductResponseSchema.model_validate(result["product"]),
        follow_up_questions=result["follow_up_questions"],
        is_complete=result["is_complete"],
    )


@router.post("/{product_id}/features", response_model=list[FeatureResponseSchema])
async def generate_feature_map(product_id: UUID, session: AsyncSession = Depends(get_session)):
    """Generate initial feature map from discovery data.

    ## Трассируемость
    Feature: F002 Feature Map Builder
    Scenarios: UC-1.2

    FR-4: Allow user to add, remove, rename, reorder feature drafts.
    """
    service = DiscoveryService(session)
    try:
        features = await service.generate_feature_map(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return [FeatureResponseSchema.model_validate(f) for f in features]


@router.post("/{product_id}/features/approve", response_model=FeatureMapResponseSchema)
async def approve_feature_map(
    product_id: UUID, data: FeatureMapApprovalSchema, session: AsyncSession = Depends(get_session)
):
    """Approve the feature map for a product.

    ## Трассируемость
    Feature: F002 Feature Map Builder
    Scenarios: UC-1.2

    FR-5: Save approved feature map as a separate versioned artifact.
    """
    service = DiscoveryService(session)
    try:
        result = await service.approve_feature_map(product_id, data.feature_ids)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return FeatureMapResponseSchema(
        product_id=product_id,
        features=[FeatureResponseSchema.model_validate(f) for f in result["features"]],
        is_approved=result["is_approved"],
    )
