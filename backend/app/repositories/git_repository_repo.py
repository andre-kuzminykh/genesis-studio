"""Repository layer for Git operations and code artifacts.

Feature: F012 GitHub Integration, F013/F014 Code Generators, F015 Deployment
"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.git_repository import GitRepository
from backend.app.models.git_operation import GitOperation, GitOperationType, GitOperationStatus
from backend.app.models.code_artifact import CodeArtifact
from backend.app.models.deployment_run import DeploymentRun, DeploymentStatus, DeploymentTarget


class GitRepositoryRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def connect(
        self, product_id: uuid.UUID, owner: str, repo_name: str, default_branch: str = "main"
    ) -> GitRepository:
        repo = GitRepository(
            product_id=product_id,
            owner=owner,
            repo_name=repo_name,
            default_branch=default_branch,
            github_url=f"https://github.com/{owner}/{repo_name}",
        )
        self.session.add(repo)
        await self.session.flush()
        return repo

    async def get_by_product(self, product_id: uuid.UUID) -> GitRepository | None:
        stmt = select(GitRepository).where(GitRepository.product_id == product_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_operation(
        self,
        repository_id: uuid.UUID,
        operation_type: GitOperationType,
        branch: str,
        **kwargs,
    ) -> GitOperation:
        op = GitOperation(repository_id=repository_id, operation_type=operation_type, branch=branch, **kwargs)
        self.session.add(op)
        await self.session.flush()
        return op

    async def update_operation_status(
        self, operation: GitOperation, status: GitOperationStatus, **kwargs
    ) -> GitOperation:
        operation.status = status
        for key, value in kwargs.items():
            if hasattr(operation, key):
                setattr(operation, key, value)
        await self.session.flush()
        return operation

    async def create_code_artifact(
        self,
        feature_id: uuid.UUID,
        prd_version_id: uuid.UUID,
        artifact_type: str,
        file_path: str,
        content_hash: str,
        description: str | None = None,
        metadata_json: dict | None = None,
    ) -> CodeArtifact:
        artifact = CodeArtifact(
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

    async def list_artifacts_by_feature(self, feature_id: uuid.UUID) -> list[CodeArtifact]:
        stmt = select(CodeArtifact).where(CodeArtifact.feature_id == feature_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_deployment_run(
        self, product_id: uuid.UUID, target: DeploymentTarget
    ) -> DeploymentRun:
        run = DeploymentRun(product_id=product_id, target=target)
        self.session.add(run)
        await self.session.flush()
        return run

    async def update_deployment_run(self, run: DeploymentRun, **kwargs) -> DeploymentRun:
        for key, value in kwargs.items():
            if hasattr(run, key):
                setattr(run, key, value)
        await self.session.flush()
        return run
