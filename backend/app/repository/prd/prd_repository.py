"""PRDRepository — persistence layer for PRD Version and all child artifacts.

This repository does NOT extend BaseRepository because it manages multiple
model types (PRDVersion, UserStory, UXFlow, UseCase, Requirement, TestCase,
Task, TraceabilityLink, ChangeRequest).

## Трассируемость
Feature: F003-F011 — PRD Generation through Change Requests
Scenarios: UC-2.1, UC-2.2, UC-3.1, UC-5.1
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.model.prd import (
    PRDVersionModel,
    UserStoryModel,
    UXFlowModel,
    UseCaseModel,
    RequirementModel,
    TestCaseModel,
    TaskModel,
    ChangeRequestModel,
    TraceabilityLinkModel,
)
from backend.app.model.enums import (
    PRDVersionStatus,
    UserStoryStatus,
    UseCaseStatus,
    TestCaseStatus,
    ChangeRequestStatus,
)


class PRDRepository:
    """Unified repository for PRD versions and all related artifacts."""

    def __init__(self, session: AsyncSession):
        self.session = session

    # ── PRD Version ──────────────────────────────────────────────────

    async def create_prd_version(
        self, feature_id: uuid.UUID, content: dict, **kwargs
    ) -> PRDVersionModel:
        # Determine next version number
        stmt = select(func.coalesce(func.max(PRDVersionModel.version_number), 0)).where(
            PRDVersionModel.feature_id == feature_id
        )
        result = await self.session.execute(stmt)
        next_version = result.scalar() + 1

        # Mark previous versions as not current
        prev_stmt = select(PRDVersionModel).where(
            PRDVersionModel.feature_id == feature_id,
            PRDVersionModel.is_current.is_(True),
        )
        prev_result = await self.session.execute(prev_stmt)
        for prev in prev_result.scalars().all():
            prev.is_current = False

        prd = PRDVersionModel(
            feature_id=feature_id,
            version_number=next_version,
            content=content,
            is_current=True,
            **kwargs,
        )
        self.session.add(prd)
        await self.session.flush()
        return prd

    async def get_current_prd_version(
        self, feature_id: uuid.UUID
    ) -> PRDVersionModel | None:
        stmt = (
            select(PRDVersionModel)
            .where(
                PRDVersionModel.feature_id == feature_id,
                PRDVersionModel.is_current.is_(True),
            )
            .options(
                selectinload(PRDVersionModel.user_stories),
                selectinload(PRDVersionModel.ux_flows),
                selectinload(PRDVersionModel.use_cases),
                selectinload(PRDVersionModel.requirements),
                selectinload(PRDVersionModel.test_cases),
                selectinload(PRDVersionModel.tasks),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def approve_prd_version(self, prd: PRDVersionModel) -> PRDVersionModel:
        prd.status = PRDVersionStatus.approved
        prd.approved_at = datetime.now(timezone.utc)
        await self.session.flush()
        return prd

    async def list_prd_versions(
        self, feature_id: uuid.UUID
    ) -> list[PRDVersionModel]:
        stmt = (
            select(PRDVersionModel)
            .where(PRDVersionModel.feature_id == feature_id)
            .order_by(PRDVersionModel.version_number.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # ── User Stories ─────────────────────────────────────────────────

    async def bulk_create_stories(
        self, prd_version_id: uuid.UUID, stories_data: list[dict]
    ) -> list[UserStoryModel]:
        stories: list[UserStoryModel] = []
        for data in stories_data:
            story = UserStoryModel(prd_version_id=prd_version_id, **data)
            self.session.add(story)
            stories.append(story)
        await self.session.flush()
        return stories

    async def approve_stories(self, story_ids: list[uuid.UUID]) -> list[UserStoryModel]:
        stmt = select(UserStoryModel).where(UserStoryModel.id.in_(story_ids))
        result = await self.session.execute(stmt)
        stories = list(result.scalars().all())
        for story in stories:
            story.status = UserStoryStatus.approved
            story.is_approved = True
        await self.session.flush()
        return stories

    # ── UX Flows ─────────────────────────────────────────────────────

    async def bulk_create_ux_flows(
        self, prd_version_id: uuid.UUID, flows_data: list[dict]
    ) -> list[UXFlowModel]:
        flows: list[UXFlowModel] = []
        for data in flows_data:
            flow = UXFlowModel(prd_version_id=prd_version_id, **data)
            self.session.add(flow)
            flows.append(flow)
        await self.session.flush()
        return flows

    # ── Use Cases ────────────────────────────────────────────────────

    async def bulk_create_use_cases(
        self, prd_version_id: uuid.UUID, cases_data: list[dict]
    ) -> list[UseCaseModel]:
        cases: list[UseCaseModel] = []
        for data in cases_data:
            case = UseCaseModel(prd_version_id=prd_version_id, **data)
            self.session.add(case)
            cases.append(case)
        await self.session.flush()
        return cases

    async def approve_use_cases(
        self, use_case_ids: list[uuid.UUID]
    ) -> list[UseCaseModel]:
        stmt = select(UseCaseModel).where(UseCaseModel.id.in_(use_case_ids))
        result = await self.session.execute(stmt)
        cases = list(result.scalars().all())
        for case in cases:
            case.status = UseCaseStatus.approved
            case.is_approved = True
        await self.session.flush()
        return cases

    # ── Requirements ─────────────────────────────────────────────────

    async def bulk_create_requirements(
        self, prd_version_id: uuid.UUID, reqs_data: list[dict]
    ) -> list[RequirementModel]:
        reqs: list[RequirementModel] = []
        for data in reqs_data:
            req = RequirementModel(prd_version_id=prd_version_id, **data)
            self.session.add(req)
            reqs.append(req)
        await self.session.flush()
        return reqs

    # ── Test Cases ───────────────────────────────────────────────────

    async def bulk_create_test_cases(
        self, prd_version_id: uuid.UUID, tests_data: list[dict]
    ) -> list[TestCaseModel]:
        tests: list[TestCaseModel] = []
        for data in tests_data:
            test = TestCaseModel(prd_version_id=prd_version_id, **data)
            self.session.add(test)
            tests.append(test)
        await self.session.flush()
        return tests

    async def approve_tests(
        self, test_ids: list[uuid.UUID]
    ) -> list[TestCaseModel]:
        stmt = select(TestCaseModel).where(TestCaseModel.id.in_(test_ids))
        result = await self.session.execute(stmt)
        tests = list(result.scalars().all())
        for test in tests:
            test.status = TestCaseStatus.approved
        await self.session.flush()
        return tests

    # ── Tasks ────────────────────────────────────────────────────────

    async def bulk_create_tasks(
        self, prd_version_id: uuid.UUID, tasks_data: list[dict]
    ) -> list[TaskModel]:
        tasks: list[TaskModel] = []
        for data in tasks_data:
            task = TaskModel(prd_version_id=prd_version_id, **data)
            self.session.add(task)
            tasks.append(task)
        await self.session.flush()
        return tasks

    # ── Traceability Links ───────────────────────────────────────────

    async def create_link(
        self,
        source_type: str,
        source_id: uuid.UUID,
        target_type: str,
        target_id: uuid.UUID,
        link_type: str,
        prd_version_id: uuid.UUID | None = None,
    ) -> TraceabilityLinkModel:
        link = TraceabilityLinkModel(
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

    async def get_links_for_prd(
        self, prd_version_id: uuid.UUID
    ) -> list[TraceabilityLinkModel]:
        stmt = select(TraceabilityLinkModel).where(
            TraceabilityLinkModel.prd_version_id == prd_version_id
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    # ── Change Requests ──────────────────────────────────────────────

    async def create_change_request(
        self,
        feature_id: uuid.UUID,
        title: str,
        description: str,
    ) -> ChangeRequestModel:
        cr = ChangeRequestModel(
            feature_id=feature_id,
            title=title,
            description=description,
        )
        self.session.add(cr)
        await self.session.flush()
        return cr

    async def approve_change_request(
        self, cr: ChangeRequestModel
    ) -> ChangeRequestModel:
        cr.status = ChangeRequestStatus.approved
        cr.resolved_at = datetime.now(timezone.utc)
        await self.session.flush()
        return cr

    async def get_change_request(
        self, cr_id: uuid.UUID
    ) -> ChangeRequestModel | None:
        stmt = select(ChangeRequestModel).where(ChangeRequestModel.id == cr_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
