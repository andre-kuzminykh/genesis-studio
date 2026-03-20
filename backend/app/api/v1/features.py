"""Feature API endpoints — PRD drafts, stories, UX, use cases, requirements, tests, code, deploy, CR.

Feature: F003-F015 (all feature-level operations)
Scenario: UC-2.1, UC-2.2, UC-3.1, UC-4.1, UC-4.2, UC-5.1
"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_session
from backend.app.schemas.prd import (
    PRDVersionResponse,
    UserStoryResponse,
    UserStoryApproval,
    UXFlowResponse,
    UseCaseResponse,
    UseCaseApproval,
    RequirementResponse,
    TestCaseResponse,
    TestApproval,
)
from backend.app.schemas.github import (
    GitHubConnectRequest,
    GitHubConnectResponse,
    CodeGenerateRequest,
    CodeGenerateResponse,
    DeployRequest,
    DeployResponse,
    ChangeRequestCreate,
    ChangeRequestResponse,
    TraceabilityResponse,
)
from backend.app.services.prd_service import PRDService
from backend.app.services.codegen_service import CodegenService
from backend.app.services.github_service import GitHubService
from backend.app.services.deploy_service import DeployService
from backend.app.services.change_request_service import ChangeRequestService

router = APIRouter(prefix="/features", tags=["Features"])


def _handle_error(e: ValueError):
    raise HTTPException(status_code=404, detail=str(e))


# --- PRD Draft ---
@router.post("/{feature_id}/prd/draft", response_model=PRDVersionResponse)
async def generate_prd_draft(feature_id: UUID, session: AsyncSession = Depends(get_session)):
    """Generate a feature-level PRD draft.

    FR-6: Collect feature-specific discovery via guided interview.
    FR-7: Generate feature-level PRD in canonical format.
    """
    try:
        result = await PRDService(session).generate_prd_draft(feature_id)
    except ValueError as e:
        _handle_error(e)
    return PRDVersionResponse.model_validate(result["prd_version"])


# --- User Stories ---
@router.post("/{feature_id}/stories/approve", response_model=list[UserStoryResponse])
async def approve_stories(
    feature_id: UUID, data: UserStoryApproval, session: AsyncSession = Depends(get_session)
):
    """Approve user stories for a feature.

    FR-8: Allow user to approve and edit stories before next stage.
    """
    try:
        result = await PRDService(session).approve_stories(feature_id, data.story_ids)
    except ValueError as e:
        _handle_error(e)
    return [UserStoryResponse.model_validate(s) for s in result["stories"]]


# --- UX Preview ---
@router.post("/{feature_id}/ux/generate", response_model=list[UXFlowResponse])
async def generate_ux(feature_id: UUID, session: AsyncSession = Depends(get_session)):
    """Generate Telegram UX preview and Mermaid diagrams.

    FR-9: Generate UX preview for Telegram with text, buttons, navigation, states.
    FR-10: Generate Mermaid user flow, sequence, and state transition diagrams.
    """
    try:
        result = await PRDService(session).generate_ux_preview(feature_id)
    except ValueError as e:
        _handle_error(e)
    return [UXFlowResponse.model_validate(f) for f in result["ux_flows"]]


# --- Use Cases ---
@router.post("/{feature_id}/use-cases/generate", response_model=list[UseCaseResponse])
async def generate_use_cases(feature_id: UUID, session: AsyncSession = Depends(get_session)):
    """Generate use cases from approved stories."""
    try:
        result = await PRDService(session).generate_use_cases(feature_id)
    except ValueError as e:
        _handle_error(e)
    return [UseCaseResponse.model_validate(uc) for uc in result["use_cases"]]


@router.post("/{feature_id}/use-cases/approve", response_model=list[UseCaseResponse])
async def approve_use_cases(
    feature_id: UUID, data: UseCaseApproval, session: AsyncSession = Depends(get_session)
):
    """Approve use cases for a feature."""
    try:
        result = await PRDService(session).approve_use_cases(feature_id, data.use_case_ids)
    except ValueError as e:
        _handle_error(e)
    return [UseCaseResponse.model_validate(uc) for uc in result["use_cases"]]


# --- Requirements ---
@router.post("/{feature_id}/requirements/generate", response_model=list[RequirementResponse])
async def generate_requirements(feature_id: UUID, session: AsyncSession = Depends(get_session)):
    """Derive FR/NFR from approved use cases.

    FR-11: Automatically derive FR and NFR from approved use cases.
    """
    try:
        result = await PRDService(session).generate_requirements(feature_id)
    except ValueError as e:
        _handle_error(e)
    return [RequirementResponse.model_validate(r) for r in result["requirements"]]


# --- Tests ---
@router.post("/{feature_id}/tests/generate", response_model=list[TestCaseResponse])
async def generate_tests(feature_id: UUID, session: AsyncSession = Depends(get_session)):
    """Generate test cases from use cases and requirements.

    FR-12: Generate tests from use cases, acceptance criteria, and edge cases.
    """
    try:
        result = await PRDService(session).generate_tests(feature_id)
    except ValueError as e:
        _handle_error(e)
    return [TestCaseResponse.model_validate(tc) for tc in result["test_cases"]]


@router.post("/{feature_id}/tests/approve", response_model=list[TestCaseResponse])
async def approve_tests(
    feature_id: UUID, data: TestApproval, session: AsyncSession = Depends(get_session)
):
    """Approve test cases for a feature."""
    try:
        result = await PRDService(session).approve_tests(feature_id, data.test_ids)
    except ValueError as e:
        _handle_error(e)
    return [TestCaseResponse.model_validate(tc) for tc in result["test_cases"]]


# --- Code Generation ---
@router.post("/{feature_id}/code/generate", response_model=CodeGenerateResponse)
async def generate_code(
    feature_id: UUID, data: CodeGenerateRequest, session: AsyncSession = Depends(get_session)
):
    """Generate backend and bot code from approved PRD.

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
    return CodeGenerateResponse(**result)


# --- GitHub ---
@router.post("/{feature_id}/github/push")
async def push_to_github(
    feature_id: UUID,
    data: CodeGenerateRequest,
    session: AsyncSession = Depends(get_session),
):
    """Push generated code to GitHub.

    NFR-13: System must not write to GitHub without explicit repo/branch selection.
    """
    from backend.app.repositories.feature_repository import FeatureRepository

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
@router.post("/{feature_id}/deploy/local", response_model=DeployResponse)
async def deploy_local(
    feature_id: UUID, data: DeployRequest, session: AsyncSession = Depends(get_session)
):
    """Deploy generated projects locally.

    FR-16: Locally deploy generated bot/service projects after codegen.
    FR-17: Form generation report and deployment report.
    """
    from backend.app.repositories.feature_repository import FeatureRepository

    feature = await FeatureRepository(session).get_by_id(feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")

    result = await DeployService(session).deploy_local(feature.product_id, data.target)
    return DeployResponse.model_validate(result)


# --- Change Request ---
@router.post("/{feature_id}/change-request", response_model=ChangeRequestResponse)
async def create_change_request(
    feature_id: UUID, data: ChangeRequestCreate, session: AsyncSession = Depends(get_session)
):
    """Create a change request for a feature.

    FR-18: Create new PRD version on every confirmed feature change.
    FR-19: Automatically calculate impact scope.
    """
    try:
        result = await ChangeRequestService(session).create_change_request(
            feature_id, data.title, data.description
        )
    except ValueError as e:
        _handle_error(e)
    return ChangeRequestResponse.model_validate(result["change_request"])


# --- Traceability ---
@router.get("/{feature_id}/traceability", response_model=TraceabilityResponse)
async def get_traceability(feature_id: UUID, session: AsyncSession = Depends(get_session)):
    """Get full traceability graph for a feature.

    NFR-10: All requirements and tests must have traceable links.
    NFR-11: Use case changes must detect affected requirements and tests.
    """
    try:
        result = await PRDService(session).get_traceability(feature_id)
    except ValueError as e:
        _handle_error(e)
    return TraceabilityResponse(**result)
