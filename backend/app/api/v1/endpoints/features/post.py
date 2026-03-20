"""Feature POST endpoints — PRD drafts, stories, UX, use cases, requirements,
tests, code generation, GitHub push, deploy, change requests.

## Трассируемость
Feature: F003-F015 (all feature-level operations)
Scenario: UC-2.1, UC-2.2, UC-3.1, UC-4.1, UC-4.2, UC-5.1
"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_session
from backend.app.schema.prd import (
    PRDVersionResponseSchema,
    UserStoryResponseSchema,
    UserStoryApprovalSchema,
    UXFlowResponseSchema,
    UseCaseResponseSchema,
    UseCaseApprovalSchema,
    RequirementResponseSchema,
    TestCaseResponseSchema,
    TestApprovalSchema,
)
from backend.app.schema.git import (
    CodeGenerateRequestSchema,
    CodeGenerateResponseSchema,
    DeployRequestSchema,
    DeployResponseSchema,
    ChangeRequestCreateSchema,
    ChangeRequestResponseSchema,
)
from backend.app.service.feature import PRDService, CodegenService, ChangeRequestService
from backend.app.service.git import GitHubService, DeployService
from backend.app.repository.feature import FeatureRepository

router = APIRouter()


def _handle_error(e: ValueError):
    raise HTTPException(status_code=404, detail=str(e))


# --- PRD Draft ---
@router.post("/{feature_id}/prd/draft", response_model=PRDVersionResponseSchema)
async def generate_prd_draft(feature_id: UUID, session: AsyncSession = Depends(get_session)):
    """Generate a feature-level PRD draft.

    ## Трассируемость
    Feature: F003 Feature PRD Generator

    FR-6: Collect feature-specific discovery via guided interview.
    FR-7: Generate feature-level PRD in canonical format.
    """
    try:
        result = await PRDService(session).generate_prd_draft(feature_id)
    except ValueError as e:
        _handle_error(e)
    return PRDVersionResponseSchema.model_validate(result["prd_version"])


# --- User Stories ---
@router.post("/{feature_id}/stories/approve", response_model=list[UserStoryResponseSchema])
async def approve_stories(
    feature_id: UUID, data: UserStoryApprovalSchema, session: AsyncSession = Depends(get_session)
):
    """Approve user stories for a feature.

    ## Трассируемость
    Feature: F004 Story Interview Engine

    FR-8: Allow user to approve and edit stories before next stage.
    """
    try:
        result = await PRDService(session).approve_stories(feature_id, data.story_ids)
    except ValueError as e:
        _handle_error(e)
    return [UserStoryResponseSchema.model_validate(s) for s in result["stories"]]


# --- UX Preview ---
@router.post("/{feature_id}/ux/generate", response_model=list[UXFlowResponseSchema])
async def generate_ux(feature_id: UUID, session: AsyncSession = Depends(get_session)):
    """Generate Telegram UX preview and Mermaid diagrams.

    ## Трассируемость
    Feature: F005 Telegram UX Preview, F006 Mermaid Flow Generator

    FR-9: Generate UX preview for Telegram with text, buttons, navigation, states.
    FR-10: Generate Mermaid user flow, sequence, and state transition diagrams.
    """
    try:
        result = await PRDService(session).generate_ux_preview(feature_id)
    except ValueError as e:
        _handle_error(e)
    return [UXFlowResponseSchema.model_validate(f) for f in result["ux_flows"]]


# --- Use Cases ---
@router.post("/{feature_id}/use-cases/generate", response_model=list[UseCaseResponseSchema])
async def generate_use_cases(feature_id: UUID, session: AsyncSession = Depends(get_session)):
    """Generate use cases from approved stories.

    ## Трассируемость
    Feature: F007 Use Case Generator
    """
    try:
        result = await PRDService(session).generate_use_cases(feature_id)
    except ValueError as e:
        _handle_error(e)
    return [UseCaseResponseSchema.model_validate(uc) for uc in result["use_cases"]]


@router.post("/{feature_id}/use-cases/approve", response_model=list[UseCaseResponseSchema])
async def approve_use_cases(
    feature_id: UUID, data: UseCaseApprovalSchema, session: AsyncSession = Depends(get_session)
):
    """Approve use cases for a feature.

    ## Трассируемость
    Feature: F007 Use Case Generator
    """
    try:
        result = await PRDService(session).approve_use_cases(feature_id, data.use_case_ids)
    except ValueError as e:
        _handle_error(e)
    return [UseCaseResponseSchema.model_validate(uc) for uc in result["use_cases"]]


# --- Requirements ---
@router.post("/{feature_id}/requirements/generate", response_model=list[RequirementResponseSchema])
async def generate_requirements(feature_id: UUID, session: AsyncSession = Depends(get_session)):
    """Derive FR/NFR from approved use cases.

    ## Трассируемость
    Feature: F008 Requirements Derivation

    FR-11: Automatically derive FR and NFR from approved use cases.
    """
    try:
        result = await PRDService(session).generate_requirements(feature_id)
    except ValueError as e:
        _handle_error(e)
    return [RequirementResponseSchema.model_validate(r) for r in result["requirements"]]


# --- Tests ---
@router.post("/{feature_id}/tests/generate", response_model=list[TestCaseResponseSchema])
async def generate_tests(feature_id: UUID, session: AsyncSession = Depends(get_session)):
    """Generate test cases from use cases and requirements.

    ## Трассируемость
    Feature: F009 Test Generator

    FR-12: Generate tests from use cases, acceptance criteria, and edge cases.
    """
    try:
        result = await PRDService(session).generate_tests(feature_id)
    except ValueError as e:
        _handle_error(e)
    return [TestCaseResponseSchema.model_validate(tc) for tc in result["test_cases"]]


@router.post("/{feature_id}/tests/approve", response_model=list[TestCaseResponseSchema])
async def approve_tests(
    feature_id: UUID, data: TestApprovalSchema, session: AsyncSession = Depends(get_session)
):
    """Approve test cases for a feature.

    ## Трассируемость
    Feature: F009 Test Generator
    """
    try:
        result = await PRDService(session).approve_tests(feature_id, data.test_ids)
    except ValueError as e:
        _handle_error(e)
    return [TestCaseResponseSchema.model_validate(tc) for tc in result["test_cases"]]


# --- Code Generation ---
@router.post("/{feature_id}/code/generate", response_model=CodeGenerateResponseSchema)
async def generate_code(
    feature_id: UUID, data: CodeGenerateRequestSchema, session: AsyncSession = Depends(get_session)
):
    """Generate backend and bot code from approved PRD.

    ## Трассируемость
    Feature: F013 Backend Code Generator, F014 Telegram Bot Code Generator

    FR-13: Generate backend code separately from Telegram bot code.
    FR-14: Use mandatory architectural codegen instruction as invariant.
    FR-15: Read repo state, perform gap analysis, make incremental changes.
    """
    try:
        result = await CodegenService(session).generate_code(
            feature_id, data.target_branch, data.commit_message
        )
    except ValueError as e:
        _handle_error(e)
    return CodeGenerateResponseSchema(**result)


# --- GitHub ---
@router.post("/{feature_id}/github/push")
async def push_to_github(
    feature_id: UUID,
    data: CodeGenerateRequestSchema,
    session: AsyncSession = Depends(get_session),
):
    """Push generated code to GitHub.

    ## Трассируемость
    Feature: F012 GitHub Integration

    NFR-13: System must not write to GitHub without explicit repo/branch selection.
    """
    feature = await FeatureRepository(session).get_by_id(feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")

    try:
        result = await GitHubService(session).push_code(
            feature_id, feature.product_id, data.target_branch, data.commit_message
        )
    except ValueError as e:
        _handle_error(e)
    return result


# --- Deploy ---
@router.post("/{feature_id}/deploy/local", response_model=DeployResponseSchema)
async def deploy_local(
    feature_id: UUID, data: DeployRequestSchema, session: AsyncSession = Depends(get_session)
):
    """Deploy generated projects locally.

    ## Трассируемость
    Feature: F015 Local Deployment Orchestrator

    FR-16: Locally deploy generated bot/service projects after codegen.
    FR-17: Form generation report and deployment report.
    """
    feature = await FeatureRepository(session).get_by_id(feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")

    result = await DeployService(session).deploy_local(feature.product_id, data.target)
    return DeployResponseSchema.model_validate(result)


# --- Change Request ---
@router.post("/{feature_id}/change-request", response_model=ChangeRequestResponseSchema)
async def create_change_request(
    feature_id: UUID, data: ChangeRequestCreateSchema, session: AsyncSession = Depends(get_session)
):
    """Create a change request for a feature.

    ## Трассируемость
    Feature: F011 PRD Versioning & Change Requests

    FR-18: Create new PRD version on every confirmed feature change.
    FR-19: Automatically calculate impact scope.
    """
    try:
        result = await ChangeRequestService(session).create_change_request(
            feature_id, data.title, data.description
        )
    except ValueError as e:
        _handle_error(e)
    return ChangeRequestResponseSchema.model_validate(result["change_request"])
