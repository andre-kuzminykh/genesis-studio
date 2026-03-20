"""Pydantic schemas for PRD Version and related artifacts.

## Трассируемость
Feature: F003 — PRD Generation
Feature: F004 — User Stories
Feature: F005 — Telegram UX Preview
Feature: F006 — Mermaid Diagrams
Feature: F007 — Use Cases
Feature: F008 — Requirements
Feature: F009 — Test Cases
Feature: F010 — Traceability Matrix
"""
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from backend.app.model.enums import (
    PRDVersionStatus,
    UserStoryStatus,
    UseCaseStatus,
    RequirementType,
    TestCaseType,
    TestCaseStatus,
)


# --- PRD Version ---
class PRDVersionResponseSchema(BaseModel):
    id: UUID
    feature_id: UUID
    version_number: int
    content: dict
    acceptance_criteria: dict | None
    status: PRDVersionStatus
    is_current: bool
    summary: str | None
    created_at: datetime
    approved_at: datetime | None

    model_config = {"from_attributes": True}


# --- User Story ---
class UserStoryResponseSchema(BaseModel):
    id: UUID
    prd_version_id: UUID
    story_id: str
    role: str
    action: str
    benefit: str
    status: UserStoryStatus
    is_approved: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserStoryApprovalSchema(BaseModel):
    story_ids: list[UUID]
    approved: bool = True


# --- UX Flow ---
class UXFlowResponseSchema(BaseModel):
    id: UUID
    prd_version_id: UUID
    flow_type: str
    title: str
    content: str
    metadata_json: dict | None
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Use Case ---
class UseCaseResponseSchema(BaseModel):
    id: UUID
    prd_version_id: UUID
    use_case_id: str
    title: str
    given: str
    when: str
    then: str
    input_spec: str | None
    output_spec: str | None
    state_transition: str | None
    edge_cases: dict | None
    status: UseCaseStatus
    is_approved: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UseCaseApprovalSchema(BaseModel):
    use_case_ids: list[UUID]
    approved: bool = True


# --- Requirement ---
class RequirementResponseSchema(BaseModel):
    id: UUID
    prd_version_id: UUID
    req_id: str
    req_type: RequirementType
    title: str
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Test Case ---
class TestCaseResponseSchema(BaseModel):
    id: UUID
    prd_version_id: UUID
    test_id: str
    title: str
    description: str
    test_type: TestCaseType
    preconditions: str | None
    steps: dict | None
    expected_result: str
    scenario_id: str | None
    status: TestCaseStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class TestApprovalSchema(BaseModel):
    test_ids: list[UUID]
    approved: bool = True


# --- Task ---
class TaskResponseSchema(BaseModel):
    id: UUID
    prd_version_id: UUID
    task_id: str
    title: str
    description: str
    task_type: str
    sort_order: int
    dependencies: dict | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
