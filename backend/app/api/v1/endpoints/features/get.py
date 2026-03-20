"""Feature GET endpoints — traceability graph.

## Трассируемость
Feature: F010 Traceability Graph
"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_session
from backend.app.schema.git import TraceabilityResponseSchema
from backend.app.service.feature import PRDService

router = APIRouter()


@router.get("/{feature_id}/traceability", response_model=TraceabilityResponseSchema)
async def get_traceability(feature_id: UUID, session: AsyncSession = Depends(get_session)):
    """Get full traceability graph for a feature.

    ## Трассируемость
    Feature: F010 Traceability Graph

    NFR-10: All requirements and tests must have traceable links.
    NFR-11: Use case changes must detect affected requirements and tests.
    """
    try:
        result = await PRDService(session).get_traceability(feature_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return TraceabilityResponseSchema(**result)
