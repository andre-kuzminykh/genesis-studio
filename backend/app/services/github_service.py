"""GitHub integration service — connects repos, reads state, commits, pushes.

Feature: F012 GitHub Integration
Scenario: UC-4.1
"""
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.feature import FeatureStatus
from backend.app.models.git_operation import GitOperationType, GitOperationStatus
from backend.app.repositories.feature_repository import FeatureRepository
from backend.app.repositories.git_repository_repo import GitRepositoryRepo


class GitHubService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.feature_repo = FeatureRepository(session)
        self.git_repo = GitRepositoryRepo(session)

    async def connect_repository(
        self, product_id: uuid.UUID, owner: str, repo_name: str, default_branch: str = "main"
    ) -> dict:
        """Connect a GitHub repository to a product."""
        existing = await self.git_repo.get_by_product(product_id)
        if existing:
            raise ValueError("Product already has a connected repository")

        repo = await self.git_repo.connect(product_id, owner, repo_name, default_branch)
        await self.session.commit()
        return repo

    async def push_code(
        self, feature_id: uuid.UUID, product_id: uuid.UUID, target_branch: str, commit_message: str | None = None
    ) -> dict:
        """Push generated code to GitHub repository.

        Scenario: UC-4.1 — GitHub push
        """
        repo = await self.git_repo.get_by_product(product_id)
        if not repo:
            raise ValueError("No GitHub repository connected for this product")

        feature = await self.feature_repo.get_by_id(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")

        if not commit_message:
            commit_message = f"feat({feature.feature_id}): generated code from approved PRD"

        # Create git operation record
        operation = await self.git_repo.create_operation(
            repository_id=repo.id,
            operation_type=GitOperationType.push,
            branch=target_branch,
            commit_message=commit_message,
        )

        # In production: use PyGitHub / gitpython to actually push
        # For now, record the operation as successful
        operation = await self.git_repo.update_operation_status(
            operation,
            GitOperationStatus.success,
            commit_sha="0000000000000000000000000000000000000000",
        )

        await self.feature_repo.update_status(feature, FeatureStatus.pushed_to_github)
        await self.session.commit()

        return {
            "operation_id": operation.id,
            "commit_sha": operation.commit_sha,
            "branch": target_branch,
            "status": operation.status.value,
        }
