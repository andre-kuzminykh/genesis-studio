"""Repository layer for PRD versions, user stories, UX flows, use cases,
requirements, test cases, tasks, and traceability links.

Feature: F003, F004, F005, F006, F007, F008, F009, F010, F011
"""
import uuid

from sqlalchemy import select, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.models.prd_version import PRDVersion, PRDVersionStatus
from backend.app.models.user_story import UserStory, UserStoryStatus
from backend.app.models.ux_flow import UXFlow
from backend.app.models.use_case import UseCase, UseCaseStatus
from backend.app.models.requirement import Requirement
from backend.app.models.test_case import TestCase, TestCaseStatus
from backend.app.models.task import Task
from backend.app.models.traceability_link import TraceabilityLink
from backend.app.models.change_request import ChangeRequest, ChangeRequestStatus


class PRDRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # --- PRD Versions ---
    async def create_prd_version(self, feature_id: uuid.UUID, content: dict, **kwargs) -> PRDVersion:
        # Determine next version number
        stmt = select(sa_func.coalesce(sa_func.max(PRDVersion.version_number), 0)).where(
            PRDVersion.feature_id == feature_id
        )
        result = await self.session.execute(stmt)
        next_version = result.scalar() + 1

        # Mark previous current as not current
        prev_stmt = select(PRDVersion).where(PRDVersion.feature_id == feature_id, PRDVersion.is_current == True)
        prev_result = await self.session.execute(prev_stmt)
        for prev in prev_result.scalars().all():
            prev.is_current = False

        prd = PRDVersion(feature_id=feature_id, version_number=next_version, content=content, **kwargs)
        self.session.add(prd)
        await self.session.flush()
        return prd

    async def get_current_prd_version(self, feature_id: uuid.UUID) -> PRDVersion | None:
        stmt = (
            select(PRDVersion)
            .options(
                selectinload(PRDVersion.user_stories),
                selectinload(PRDVersion.ux_flows),
                selectinload(PRDVersion.use_cases),
                selectinload(PRDVersion.requirements),
                selectinload(PRDVersion.test_cases),
                selectinload(PRDVersion.tasks),
            )
            .where(PRDVersion.feature_id == feature_id, PRDVersion.is_current == True)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def approve_prd_version(self, prd: PRDVersion) -> PRDVersion:
        from datetime import datetime, timezone
        prd.status = PRDVersionStatus.approved
        prd.approved_at = datetime.now(timezone.utc)
        await self.session.flush()
        return prd

    async def list_prd_versions(self, feature_id: uuid.UUID) -> list[PRDVersion]:
        stmt = select(PRDVersion).where(PRDVersion.feature_id == feature_id).order_by(PRDVersion.version_number)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # --- User Stories ---
    async def bulk_create_stories(self, prd_version_id: uuid.UUID, stories_data: list[dict]) -> list[UserStory]:
        stories = []
        for i, sd in enumerate(stories_data):
            story = UserStory(
                prd_version_id=prd_version_id,
                story_id=sd.get("story_id", f"US-{i+1}"),
                role=sd["role"],
                action=sd["action"],
                benefit=sd["benefit"],
            )
            self.session.add(story)
            stories.append(story)
        await self.session.flush()
        return stories

    async def approve_stories(self, story_ids: list[uuid.UUID]) -> list[UserStory]:
        stmt = select(UserStory).where(UserStory.id.in_(story_ids))
        result = await self.session.execute(stmt)
        stories = list(result.scalars().all())
        for story in stories:
            story.status = UserStoryStatus.approved
            story.is_approved = True
        await self.session.flush()
        return stories

    # --- UX Flows ---
    async def bulk_create_ux_flows(self, prd_version_id: uuid.UUID, flows_data: list[dict]) -> list[UXFlow]:
        flows = []
        for fd in flows_data:
            flow = UXFlow(
                prd_version_id=prd_version_id,
                flow_type=fd["flow_type"],
                title=fd["title"],
                content=fd["content"],
                metadata_json=fd.get("metadata_json"),
            )
            self.session.add(flow)
            flows.append(flow)
        await self.session.flush()
        return flows

    # --- Use Cases ---
    async def bulk_create_use_cases(self, prd_version_id: uuid.UUID, cases_data: list[dict]) -> list[UseCase]:
        cases = []
        for i, cd in enumerate(cases_data):
            case = UseCase(
                prd_version_id=prd_version_id,
                use_case_id=cd.get("use_case_id", f"UC-{i+1}"),
                title=cd["title"],
                given=cd["given"],
                when=cd["when"],
                then=cd["then"],
                input_spec=cd.get("input_spec"),
                output_spec=cd.get("output_spec"),
                state_transition=cd.get("state_transition"),
                edge_cases=cd.get("edge_cases"),
            )
            self.session.add(case)
            cases.append(case)
        await self.session.flush()
        return cases

    async def approve_use_cases(self, use_case_ids: list[uuid.UUID]) -> list[UseCase]:
        stmt = select(UseCase).where(UseCase.id.in_(use_case_ids))
        result = await self.session.execute(stmt)
        cases = list(result.scalars().all())
        for case in cases:
            case.status = UseCaseStatus.approved
            case.is_approved = True
        await self.session.flush()
        return cases

    # --- Requirements ---
    async def bulk_create_requirements(self, prd_version_id: uuid.UUID, reqs_data: list[dict]) -> list[Requirement]:
        reqs = []
        for i, rd in enumerate(reqs_data):
            req = Requirement(
                prd_version_id=prd_version_id,
                req_id=rd.get("req_id", f"REQ-{i+1}"),
                req_type=rd["req_type"],
                title=rd["title"],
                description=rd["description"],
            )
            self.session.add(req)
            reqs.append(req)
        await self.session.flush()
        return reqs

    # --- Test Cases ---
    async def bulk_create_test_cases(self, prd_version_id: uuid.UUID, tests_data: list[dict]) -> list[TestCase]:
        tests = []
        for i, td in enumerate(tests_data):
            test = TestCase(
                prd_version_id=prd_version_id,
                test_id=td.get("test_id", f"TC-{i+1}"),
                title=td["title"],
                description=td["description"],
                test_type=td.get("test_type", "unit"),
                preconditions=td.get("preconditions"),
                steps=td.get("steps"),
                expected_result=td["expected_result"],
                scenario_id=td.get("scenario_id"),
            )
            self.session.add(test)
            tests.append(test)
        await self.session.flush()
        return tests

    async def approve_tests(self, test_ids: list[uuid.UUID]) -> list[TestCase]:
        stmt = select(TestCase).where(TestCase.id.in_(test_ids))
        result = await self.session.execute(stmt)
        tests = list(result.scalars().all())
        for test in tests:
            test.status = TestCaseStatus.approved
        await self.session.flush()
        return tests

    # --- Tasks ---
    async def bulk_create_tasks(self, prd_version_id: uuid.UUID, tasks_data: list[dict]) -> list[Task]:
        tasks = []
        for i, td in enumerate(tasks_data):
            task = Task(
                prd_version_id=prd_version_id,
                task_id=td.get("task_id", f"T-{i+1}"),
                title=td["title"],
                description=td["description"],
                task_type=td.get("task_type", "backend"),
                sort_order=td.get("sort_order", i),
                dependencies=td.get("dependencies"),
            )
            self.session.add(task)
            tasks.append(task)
        await self.session.flush()
        return tasks

    # --- Traceability Links ---
    async def create_link(
        self,
        source_type: str,
        source_id: uuid.UUID,
        target_type: str,
        target_id: uuid.UUID,
        link_type: str = "derives_from",
        prd_version_id: uuid.UUID | None = None,
    ) -> TraceabilityLink:
        link = TraceabilityLink(
            source_type=source_type,
            source_id=source_id,
            target_type=target_type,
            target_id=target_id,
            link_type=link_type,
            prd_version_id=prd_version_id,
        )
        self.session.add(link)
        await self.session.flush()
        return link

    async def get_links_for_prd(self, prd_version_id: uuid.UUID) -> list[TraceabilityLink]:
        stmt = select(TraceabilityLink).where(TraceabilityLink.prd_version_id == prd_version_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # --- Change Requests ---
    async def create_change_request(
        self, feature_id: uuid.UUID, title: str, description: str
    ) -> ChangeRequest:
        cr = ChangeRequest(feature_id=feature_id, title=title, description=description)
        self.session.add(cr)
        await self.session.flush()
        return cr

    async def approve_change_request(self, cr: ChangeRequest) -> ChangeRequest:
        from datetime import datetime, timezone
        cr.status = ChangeRequestStatus.approved
        cr.resolved_at = datetime.now(timezone.utc)
        await self.session.flush()
        return cr

    async def get_change_request(self, cr_id: uuid.UUID) -> ChangeRequest | None:
        stmt = select(ChangeRequest).where(ChangeRequest.id == cr_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
