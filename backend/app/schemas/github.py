"""Pydantic schemas for GitHub and deployment operations."""
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class GitHubConnectRequest(BaseModel):
    owner: str = Field(..., max_length=255)
    repo_name: str = Field(..., max_length=255)
    default_branch: str = Field("main", max_length=100)


class GitHubConnectResponse(BaseModel):
    id: UUID
    product_id: UUID
    owner: str
    repo_name: str
    default_branch: str
    github_url: str
    created_at: datetime

    model_config = {"from_attributes": True}


class CodeGenerateRequest(BaseModel):
    target_branch: str = Field("main", max_length=255)
    commit_message: str | None = None


class CodeGenerateResponse(BaseModel):
    feature_id: UUID
    prd_version_id: UUID
    artifacts_count: int
    commit_sha: str | None
    push_status: str
    generation_report: dict


class DeployRequest(BaseModel):
    target: str = Field("both", description="backend, bot, or both")


class DeployResponse(BaseModel):
    id: UUID
    product_id: UUID
    target: str
    status: str
    endpoints: dict | None
    logs: str | None
    error_message: str | None
    report: dict | None
    created_at: datetime
    finished_at: datetime | None

    model_config = {"from_attributes": True}


class ChangeRequestCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: str


class ChangeRequestResponse(BaseModel):
    id: UUID
    feature_id: UUID
    title: str
    description: str
    impact_analysis: dict | None
    diff_summary: dict | None
    status: str
    created_at: datetime
    resolved_at: datetime | None

    model_config = {"from_attributes": True}


class TraceabilityResponse(BaseModel):
    feature_id: UUID
    prd_version_id: UUID
    user_stories_count: int
    use_cases_count: int
    requirements_count: int
    test_cases_count: int
    tasks_count: int
    code_artifacts_count: int
    links: list[dict]
