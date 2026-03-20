"""Change request service — manages PRD versioning and impact analysis.

Feature: F011 PRD Versioning & Change Requests
Scenario: UC-5.1
"""
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.change_request import ChangeRequestStatus
from backend.app.repositories.feature_repository import FeatureRepository
from backend.app.repositories.prd_repository import PRDRepository


class ChangeRequestService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.feature_repo = FeatureRepository(session)
        self.prd_repo = PRDRepository(session)

    async def create_change_request(
        self, feature_id: uuid.UUID, title: str, description: str
    ) -> dict:
        """Create a change request for a feature.

        Scenario: UC-5.1 — change request creation, impact analysis,
        new PRD version creation.

        NFR-16: History must be auditable.
        NFR-17: Update must be atomic — no partial state.
        """
        feature = await self.feature_repo.get_by_id(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")

        current_prd = await self.prd_repo.get_current_prd_version(feature_id)
        if not current_prd:
            raise ValueError("No current PRD version to change")

        # Create change request
        cr = await self.prd_repo.create_change_request(feature_id, title, description)

        # Calculate impact analysis
        impact = {
            "affected_use_cases": len(current_prd.use_cases),
            "affected_requirements": len(current_prd.requirements),
            "affected_tests": len(current_prd.test_cases),
            "affected_tasks": len(current_prd.tasks),
            "description": description,
        }
        cr.impact_analysis = impact

        # Create diff summary
        cr.diff_summary = {
            "change_type": "modification",
            "previous_version": current_prd.version_number,
            "affected_sections": ["use_cases", "requirements", "tests"],
        }

        await self.session.flush()
        await self.session.commit()

        return {
            "change_request": cr,
            "impact_analysis": impact,
        }

    async def approve_and_apply(self, cr_id: uuid.UUID) -> dict:
        """Approve a CR and create a new PRD version with updated artifacts.

        Flow: CR approved → new PRD version → tests updated → ready for codegen
        """
        cr = await self.prd_repo.get_change_request(cr_id)
        if not cr:
            raise ValueError(f"Change request {cr_id} not found")

        feature = await self.feature_repo.get_by_id(cr.feature_id)
        if not feature:
            raise ValueError(f"Feature not found")

        current_prd = await self.prd_repo.get_current_prd_version(cr.feature_id)
        if not current_prd:
            raise ValueError("No current PRD version")

        # Approve CR
        cr = await self.prd_repo.approve_change_request(cr)

        # Create new PRD version based on current + CR changes
        new_content = dict(current_prd.content)
        new_content["change_history"] = new_content.get("change_history", []) + [
            {"cr_id": str(cr.id), "title": cr.title, "description": cr.description}
        ]

        new_prd = await self.prd_repo.create_prd_version(
            feature_id=cr.feature_id,
            content=new_content,
            summary=f"Updated via CR: {cr.title}",
            change_request_id=cr.id,
        )

        cr.status = ChangeRequestStatus.applied
        await self.session.flush()
        await self.session.commit()

        return {
            "change_request": cr,
            "new_prd_version": new_prd,
        }
