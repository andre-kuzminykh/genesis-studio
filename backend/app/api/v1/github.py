"""GitHub connection endpoint.

Feature: F012 GitHub Integration
"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_session
from backend.app.schemas.github import GitHubConnectRequest, GitHubConnectResponse
from backend.app.services.github_service import GitHubService

router = APIRouter(prefix="/github", tags=["GitHub"])


@router.post("/connect/{product_id}", response_model=GitHubConnectResponse, status_code=201)
async def connect_github(
    product_id: UUID, data: GitHubConnectRequest, session: AsyncSession = Depends(get_session)
):
    """Connect a GitHub repository to a product.

    NFR-13: System must not write to GitHub without explicit repo/branch selection.
    """
    service = GitHubService(session)
    try:
        repo = await service.connect_repository(
            product_id, data.owner, data.repo_name, data.default_branch
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return GitHubConnectResponse.model_validate(repo)
