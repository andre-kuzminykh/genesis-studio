"""Features API client — feature-level backend operations.

## Трассируемость
Feature: F002-F015 — Feature lifecycle actions
"""
from uuid import UUID

import httpx

from bot.core.config import bot_settings


class FeaturesAPI:
    def __init__(self):
        self.base_url = bot_settings.backend_url.rstrip("/")

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30.0) as client:
            response = await client.request(method, path, **kwargs)
            response.raise_for_status()
            return response.json()

    async def generate_prd_draft(self, feature_id: UUID | str) -> dict:
        return await self._request(
            "POST", f"/api/v1/features/{feature_id}/prd/draft"
        )

    async def approve_stories(
        self, feature_id: UUID | str, story_ids: list[str]
    ) -> list[dict]:
        return await self._request(
            "POST",
            f"/api/v1/features/{feature_id}/stories/approve",
            json={"story_ids": story_ids, "approved": True},
        )

    async def generate_ux(self, feature_id: UUID | str) -> list[dict]:
        return await self._request(
            "POST", f"/api/v1/features/{feature_id}/ux/generate"
        )

    async def generate_use_cases(self, feature_id: UUID | str) -> list[dict]:
        return await self._request(
            "POST", f"/api/v1/features/{feature_id}/use-cases/generate"
        )

    async def approve_use_cases(
        self, feature_id: UUID | str, use_case_ids: list[str]
    ) -> list[dict]:
        return await self._request(
            "POST",
            f"/api/v1/features/{feature_id}/use-cases/approve",
            json={"use_case_ids": use_case_ids, "approved": True},
        )

    async def generate_requirements(self, feature_id: UUID | str) -> list[dict]:
        return await self._request(
            "POST", f"/api/v1/features/{feature_id}/requirements/generate"
        )

    async def generate_tests(self, feature_id: UUID | str) -> list[dict]:
        return await self._request(
            "POST", f"/api/v1/features/{feature_id}/tests/generate"
        )

    async def approve_tests(
        self, feature_id: UUID | str, test_ids: list[str]
    ) -> list[dict]:
        return await self._request(
            "POST",
            f"/api/v1/features/{feature_id}/tests/approve",
            json={"test_ids": test_ids, "approved": True},
        )

    async def generate_code(
        self, feature_id: UUID | str, target_branch: str = "main"
    ) -> dict:
        return await self._request(
            "POST",
            f"/api/v1/features/{feature_id}/code/generate",
            json={"target_branch": target_branch},
        )

    async def push_to_github(
        self, feature_id: UUID | str, target_branch: str = "main"
    ) -> dict:
        return await self._request(
            "POST",
            f"/api/v1/features/{feature_id}/github/push",
            json={"target_branch": target_branch},
        )

    async def deploy_local(
        self, feature_id: UUID | str, target: str = "both"
    ) -> dict:
        return await self._request(
            "POST",
            f"/api/v1/features/{feature_id}/deploy/local",
            json={"target": target},
        )

    async def create_change_request(
        self, feature_id: UUID | str, title: str, description: str
    ) -> dict:
        return await self._request(
            "POST",
            f"/api/v1/features/{feature_id}/change-request",
            json={"title": title, "description": description},
        )

    async def get_traceability(self, feature_id: UUID | str) -> dict:
        return await self._request(
            "GET", f"/api/v1/features/{feature_id}/traceability"
        )
