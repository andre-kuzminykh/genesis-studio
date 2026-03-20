"""Pydantic schemas for GitHub and deployment operations.

## Трассируемость
Feature: F012 — GitHub Integration
Feature: F013 — Code Generation
Feature: F014 — Code Artifact Management
Feature: F015 — Local Deployment
"""
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class GitHubConnectRequestSchema(BaseModel):
    owner: str = Field(..., max_length=255)
    repo_name: str = Field(..., max_length=255)
    default_branch: str = Field("main", max_length=100)


class GitHubConnectResponseSchema(BaseModel):
    id: UUID
    product_id: UUID
    owner: str
    repo_name: str
    default_branch: str
    github_url: str
    created_at: datetime

    model_config = {"from_attributes": True}


class CodeGenerateRequestSchema(BaseModel):
    target_branch: str = Field("main", max_length=255)
    commit_message: str | None = None


class CodeGenerateResponseSchema(BaseModel):
    feature_id: UUID
    prd_version_id: UUID
    artifacts_count: int
    commit_sha: str | None
    push_status: str
    generation_report: dict


class DeployRequestSchema(BaseModel):
    target: str = Field("both", description="backend, bot, or both")


class DeployResponseSchema(BaseModel):
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


class ChangeRequestCreateSchema(BaseModel):
    title: str = Field(..., max_length=255)
    description: str


class ChangeRequestResponseSchema(BaseModel):
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


class TraceabilityResponseSchema(BaseModel):
    feature_id: UUID
    prd_version_id: UUID
    user_stories_count: int
    use_cases_count: int
    requirements_count: int
    test_cases_count: int
    tasks_count: int
    code_artifacts_count: int
    links: list[dict]
