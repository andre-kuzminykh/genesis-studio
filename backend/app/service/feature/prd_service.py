"""PRD service — handles feature-level PRD generation, stories, UX, use cases,
requirements, tests, and tasks derivation.

## Трассируемость
Feature: F003 Feature PRD Generator, F004 Story Interview Engine,
F005 Telegram UX Preview, F006 Mermaid Flow Generator,
F007 Use Case Generator, F008 Requirements Derivation,
F009 Test Generator, F010 Traceability Graph
Scenario: UC-2.1, UC-2.2, UC-3.1
"""
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.model.enums import FeatureStatus
from backend.app.repository.feature import FeatureRepository
from backend.app.repository.prd import PRDRepository


class PRDService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.feature_repo = FeatureRepository(session)
        self.prd_repo = PRDRepository(session)

    async def generate_prd_draft(self, feature_id: uuid.UUID) -> dict:
        """Generate a feature-level PRD draft with user stories.

        Scenario: UC-2.1 — feature interview → PRD draft creation
        """
        feature = await self.feature_repo.get_by_id(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")

        # Generate PRD content (in production, this calls LLM)
        prd_content = {
            "feature_id": feature.feature_id,
            "feature_name": feature.name,
            "overview": feature.overview or "",
            "context": f"Feature {feature.feature_id} of product {feature.product_id}",
            "business_rules": [],
            "acceptance_criteria": [],
        }

        prd_version = await self.prd_repo.create_prd_version(
            feature_id=feature_id,
            content=prd_content,
            summary=f"Initial PRD draft for {feature.name}",
        )

        # Generate initial user stories
        stories_data = [
            {
                "story_id": f"US-{feature.feature_id}-1",
                "role": "user",
                "action": f"use the {feature.name} feature",
                "benefit": "accomplish the primary goal efficiently",
            },
            {
                "story_id": f"US-{feature.feature_id}-2",
                "role": "admin",
                "action": f"manage {feature.name} settings",
                "benefit": "customize behavior for different use cases",
            },
        ]
        stories = await self.prd_repo.bulk_create_stories(prd_version.id, stories_data)

        await self.feature_repo.update_status(feature, FeatureStatus.prd_draft_created)
        await self.session.commit()

        return {"prd_version": prd_version, "user_stories": stories}

    async def approve_stories(self, feature_id: uuid.UUID, story_ids: list[uuid.UUID]) -> dict:
        """Approve user stories for a feature PRD.

        Scenario: UC-2.1 — user stories approval
        """
        feature = await self.feature_repo.get_by_id(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")

        stories = await self.prd_repo.approve_stories(story_ids)
        await self.feature_repo.update_status(feature, FeatureStatus.stories_approved)
        await self.session.commit()

        return {"stories": stories}

    async def generate_ux_preview(self, feature_id: uuid.UUID) -> dict:
        """Generate Telegram UX preview and Mermaid diagrams.

        Scenario: UC-2.2 — UX preview and Mermaid generation
        """
        feature = await self.feature_repo.get_by_id(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")

        prd = await self.prd_repo.get_current_prd_version(feature_id)
        if not prd:
            raise ValueError("No current PRD version found")

        # Generate UX flows (in production, LLM-generated)
        flows_data = [
            {
                "flow_type": "telegram_preview",
                "title": f"Telegram UI — {feature.name}",
                "content": (
                    f"Screen: {feature.name}\n"
                    f"[Button: Start] [Button: Settings]\n"
                    f"Message: Welcome to {feature.name}\n"
                    f"[Inline: Action 1] [Inline: Action 2]"
                ),
                "metadata_json": {"screens": 2, "buttons": 4},
            },
            {
                "flow_type": "mermaid_user_flow",
                "title": f"User Flow — {feature.name}",
                "content": (
                    f"graph TD\n"
                    f"    A[Start] --> B{{Choose Action}}\n"
                    f"    B --> C[Action 1]\n"
                    f"    B --> D[Action 2]\n"
                    f"    C --> E[Result]\n"
                    f"    D --> E"
                ),
            },
            {
                "flow_type": "mermaid_sequence",
                "title": f"Sequence — {feature.name}",
                "content": (
                    f"sequenceDiagram\n"
                    f"    User->>Bot: /start\n"
                    f"    Bot->>Backend: POST /api/v1/action\n"
                    f"    Backend-->>Bot: Response\n"
                    f"    Bot-->>User: Result message"
                ),
            },
            {
                "flow_type": "mermaid_state",
                "title": f"State — {feature.name}",
                "content": (
                    f"stateDiagram-v2\n"
                    f"    [*] --> Idle\n"
                    f"    Idle --> Processing: user_action\n"
                    f"    Processing --> Complete: success\n"
                    f"    Processing --> Error: failure\n"
                    f"    Complete --> [*]\n"
                    f"    Error --> Idle: retry"
                ),
            },
        ]

        ux_flows = await self.prd_repo.bulk_create_ux_flows(prd.id, flows_data)
        await self.feature_repo.update_status(feature, FeatureStatus.ux_approved)
        await self.session.commit()

        return {"ux_flows": ux_flows}

    async def generate_use_cases(self, feature_id: uuid.UUID) -> dict:
        """Generate use cases from approved stories.

        Scenario: UC-2.2 — use case generation
        """
        feature = await self.feature_repo.get_by_id(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")

        prd = await self.prd_repo.get_current_prd_version(feature_id)
        if not prd:
            raise ValueError("No current PRD version found")

        # Generate use cases (in production, LLM-generated from stories)
        cases_data = [
            {
                "use_case_id": f"UC-{feature.feature_id}-1",
                "title": f"Main happy path for {feature.name}",
                "given": "User is authenticated and on the main screen",
                "when": f"User initiates {feature.name} action",
                "then": "System processes request and returns success result",
                "input_spec": "User action payload",
                "output_spec": "Success response with result data",
                "state_transition": "idle → processing → complete",
            },
            {
                "use_case_id": f"UC-{feature.feature_id}-2",
                "title": f"Error handling for {feature.name}",
                "given": "User is authenticated and on the main screen",
                "when": f"User initiates {feature.name} with invalid data",
                "then": "System returns validation error with user-friendly message",
                "input_spec": "Invalid user payload",
                "output_spec": "Error response with remediation hint",
                "state_transition": "idle → processing → error → idle",
                "edge_cases": {"empty_input": "Return specific empty input message"},
            },
        ]

        use_cases = await self.prd_repo.bulk_create_use_cases(prd.id, cases_data)
        await self.session.commit()

        return {"use_cases": use_cases}

    async def approve_use_cases(self, feature_id: uuid.UUID, use_case_ids: list[uuid.UUID]) -> dict:
        """Approve use cases for a feature.

        Scenario: UC-2.2 — use case approval
        """
        feature = await self.feature_repo.get_by_id(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")

        cases = await self.prd_repo.approve_use_cases(use_case_ids)
        await self.feature_repo.update_status(feature, FeatureStatus.use_cases_approved)
        await self.session.commit()

        return {"use_cases": cases}

    async def generate_requirements(self, feature_id: uuid.UUID) -> dict:
        """Derive FR/NFR from approved use cases.

        Scenario: UC-3.1 — requirements derivation
        """
        feature = await self.feature_repo.get_by_id(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")

        prd = await self.prd_repo.get_current_prd_version(feature_id)
        if not prd:
            raise ValueError("No current PRD version found")

        # Generate requirements (in production, LLM-derived from use cases)
        reqs_data = [
            {
                "req_id": f"FR-{feature.feature_id}-1",
                "req_type": "functional",
                "title": f"Core {feature.name} processing",
                "description": f"System must process {feature.name} requests and return results within SLA",
            },
            {
                "req_id": f"FR-{feature.feature_id}-2",
                "req_type": "functional",
                "title": f"Input validation for {feature.name}",
                "description": "System must validate all inputs and return structured error messages",
            },
            {
                "req_id": f"NFR-{feature.feature_id}-1",
                "req_type": "non_functional",
                "title": "Response time",
                "description": "API response time must be ≤ 2 seconds for standard operations",
            },
            {
                "req_id": f"NFR-{feature.feature_id}-2",
                "req_type": "non_functional",
                "title": "Data integrity",
                "description": "All operations must be atomic; partial updates are not acceptable",
            },
        ]

        requirements = await self.prd_repo.bulk_create_requirements(prd.id, reqs_data)

        # Create traceability links: use_cases → requirements
        for uc in prd.use_cases:
            for req in requirements:
                await self.prd_repo.create_link(
                    source_type="use_case", source_id=uc.id,
                    target_type="requirement", target_id=req.id,
                    link_type="derives_from", prd_version_id=prd.id,
                )

        await self.feature_repo.update_status(feature, FeatureStatus.requirements_generated)
        await self.session.commit()

        return {"requirements": requirements}

    async def generate_tests(self, feature_id: uuid.UUID) -> dict:
        """Generate test cases from use cases and requirements.

        Scenario: UC-3.1 — test generation
        """
        feature = await self.feature_repo.get_by_id(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")

        prd = await self.prd_repo.get_current_prd_version(feature_id)
        if not prd:
            raise ValueError("No current PRD version found")

        # Generate tests (in production, LLM-generated from use cases + requirements)
        tests_data = [
            {
                "test_id": f"TC-{feature.feature_id}-1",
                "title": f"Test happy path — {feature.name}",
                "description": f"Verify main use case of {feature.name} succeeds",
                "test_type": "integration",
                "expected_result": "Request processed successfully, correct response returned",
                "scenario_id": f"UC-{feature.feature_id}-1",
            },
            {
                "test_id": f"TC-{feature.feature_id}-2",
                "title": f"Test validation — {feature.name}",
                "description": f"Verify invalid input handling for {feature.name}",
                "test_type": "unit",
                "expected_result": "Validation error returned with descriptive message",
                "scenario_id": f"UC-{feature.feature_id}-2",
            },
            {
                "test_id": f"TC-{feature.feature_id}-3",
                "title": f"Test performance — {feature.name}",
                "description": f"Verify response time SLA for {feature.name}",
                "test_type": "integration",
                "expected_result": "Response time ≤ 2 seconds",
                "scenario_id": f"UC-{feature.feature_id}-1",
            },
        ]

        test_cases = await self.prd_repo.bulk_create_test_cases(prd.id, tests_data)

        # Create traceability links: use_cases → tests
        for tc in test_cases:
            for uc in prd.use_cases:
                await self.prd_repo.create_link(
                    source_type="use_case", source_id=uc.id,
                    target_type="test_case", target_id=tc.id,
                    link_type="tested_by", prd_version_id=prd.id,
                )

        await self.feature_repo.update_status(feature, FeatureStatus.tests_generated)
        await self.session.commit()

        return {"test_cases": test_cases}

    async def approve_tests(self, feature_id: uuid.UUID, test_ids: list[uuid.UUID]) -> dict:
        """Approve test cases for a feature."""
        feature = await self.feature_repo.get_by_id(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")

        tests = await self.prd_repo.approve_tests(test_ids)
        await self.feature_repo.update_status(feature, FeatureStatus.tests_approved)
        await self.session.commit()

        return {"test_cases": tests}

    async def get_traceability(self, feature_id: uuid.UUID) -> dict:
        """Get full traceability graph for a feature.

        Feature: F010 Traceability Graph
        """
        prd = await self.prd_repo.get_current_prd_version(feature_id)
        if not prd:
            raise ValueError("No current PRD version found")

        links = await self.prd_repo.get_links_for_prd(prd.id)

        return {
            "feature_id": feature_id,
            "prd_version_id": prd.id,
            "user_stories_count": len(prd.user_stories),
            "use_cases_count": len(prd.use_cases),
            "requirements_count": len(prd.requirements),
            "test_cases_count": len(prd.test_cases),
            "tasks_count": len(prd.tasks),
            "code_artifacts_count": 0,
            "links": [
                {
                    "source_type": link.source_type,
                    "source_id": str(link.source_id),
                    "target_type": link.target_type,
                    "target_id": str(link.target_id),
                    "link_type": link.link_type,
                }
                for link in links
            ],
        }
