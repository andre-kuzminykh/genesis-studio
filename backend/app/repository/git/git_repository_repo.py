"""GitRepositoryRepo — persistence layer for Git integration entities.

## Трассируемость
Feature: F012 — GitHub Integration
Feature: F013 — Code Generation
Feature: F014 — Code Artifact Management
Feature: F015 — Local Deployment
"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.model.git import (
    GitRepositoryModel,
    GitOperationModel,
    CodeArtifactModel,
    DeploymentRunModel,
)


class GitRepositoryRepo:
    """Repository for Git-related models (repository, operations, artifacts, deployments)."""

    def __init__(self, session: AsyncSession):
        self.session = session

    # ── Git Repository ───────────────────────────────────────────────

    async def connect(
        self,
        product_id: uuid.UUID,
        owner: str,
        repo_name: str,
        default_branch: str = "main",
    ) -> GitRepositoryModel:
        repo = GitRepositoryModel(
            product_id=product_id,
            owner=owner,
            repo_name=repo_name,
            default_branch=default_branch,
            github_url=f"https://github.com/{owner}/{repo_name}",
        )
        self.session.add(repo)
        await self.session.flush()
        return repo

    async def get_by_product(
        self, product_id: uuid.UUID
    ) -> GitRepositoryModel | None:
        stmt = select(GitRepositoryModel).where(
            GitRepositoryModel.product_id == product_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    # ── Git Operations ───────────────────────────────────────────────

    async def create_operation(
        self,
        repository_id: uuid.UUID,
        operation_type,
        branch: str,
        **kwargs,
    ) -> GitOperationModel:
        operation = GitOperationModel(
            repository_id=repository_id,
            operation_type=operation_type,
            branch=branch,
            **kwargs,
        )
        self.session.add(operation)
        await self.session.flush()
        return operation

    async def update_operation_status(
        self, operation: GitOperationModel, status, **kwargs
    ) -> GitOperationModel:
        operation.status = status
        for key, value in kwargs.items():
            if hasattr(operation, key):
                setattr(operation, key, value)
        await self.session.flush()
        return operation

    # ── Code Artifacts ───────────────────────────────────────────────

    async def create_code_artifact(
        self,
        feature_id: uuid.UUID,
        prd_version_id: uuid.UUID,
        artifact_type,
        file_path: str,
        content_hash: str,
        description: str | None = None,
        metadata_json: dict | None = None,
    ) -> CodeArtifactModel:
        artifact = CodeArtifactModel(
            feature_id=feature_id,
            prd_version_id=prd_version_id,
            artifact_type=artifact_type,
            file_path=file_path,
            content_hash=content_hash,
            description=description,
            metadata_json=metadata_json,
        )
        self.session.add(artifact)
        await self.session.flush()
        return artifact

    async def list_artifacts_by_feature(
        self, feature_id: uuid.UUID
    ) -> list[CodeArtifactModel]:
        stmt = select(CodeArtifactModel).where(
            CodeArtifactModel.feature_id == feature_id
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # ── Deployment Runs ──────────────────────────────────────────────

    async def create_deployment_run(
        self, product_id: uuid.UUID, target
    ) -> DeploymentRunModel:
        run = DeploymentRunModel(
            product_id=product_id,
            target=target,
        )
        self.session.add(run)
        await self.session.flush()
        return run

    async def update_deployment_run(
        self, run: DeploymentRunModel, **kwargs
    ) -> DeploymentRunModel:
        for key, value in kwargs.items():
            if hasattr(run, key):
                setattr(run, key, value)
        await self.session.flush()
        return run
