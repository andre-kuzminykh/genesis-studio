"""Backend API client for the Telegram bot.

Bot architecture: all data access goes through backend HTTP API.
Bot = UI only, no direct DB access.
"""
from uuid import UUID

import httpx

from bot.core.config import bot_settings


class BackendAPIClient:
    def __init__(self):
        self.base_url = bot_settings.backend_url.rstrip("/")

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30.0) as client:
            response = await client.request(method, path, **kwargs)
            response.raise_for_status()
            return response.json()

    # --- Products ---
    async def create_product(self, idea_text: str, name: str | None = None) -> dict:
        return await self._request("POST", "/api/v1/products", json={"idea_text": idea_text, "name": name})

    async def submit_discovery(self, product_id: UUID, question: str, answer: str) -> dict:
        return await self._request(
            "POST", f"/api/v1/products/{product_id}/discovery",
            json={"question": question, "answer": answer},
        )

    async def generate_feature_map(self, product_id: UUID) -> list[dict]:
        return await self._request("POST", f"/api/v1/products/{product_id}/features")

    async def approve_feature_map(self, product_id: UUID, feature_ids: list[str]) -> dict:
        return await self._request(
            "POST", f"/api/v1/products/{product_id}/features/approve",
            json={"feature_ids": feature_ids},
        )

    # --- Features ---
    async def generate_prd_draft(self, feature_id: UUID) -> dict:
        return await self._request("POST", f"/api/v1/features/{feature_id}/prd/draft")

    async def approve_stories(self, feature_id: UUID, story_ids: list[str]) -> list[dict]:
        return await self._request(
            "POST", f"/api/v1/features/{feature_id}/stories/approve",
            json={"story_ids": story_ids, "approved": True},
        )

    async def generate_ux(self, feature_id: UUID) -> list[dict]:
        return await self._request("POST", f"/api/v1/features/{feature_id}/ux/generate")

    async def generate_use_cases(self, feature_id: UUID) -> list[dict]:
        return await self._request("POST", f"/api/v1/features/{feature_id}/use-cases/generate")

    async def approve_use_cases(self, feature_id: UUID, use_case_ids: list[str]) -> list[dict]:
        return await self._request(
            "POST", f"/api/v1/features/{feature_id}/use-cases/approve",
            json={"use_case_ids": use_case_ids, "approved": True},
        )

    async def generate_requirements(self, feature_id: UUID) -> list[dict]:
        return await self._request("POST", f"/api/v1/features/{feature_id}/requirements/generate")

    async def generate_tests(self, feature_id: UUID) -> list[dict]:
        return await self._request("POST", f"/api/v1/features/{feature_id}/tests/generate")

    async def approve_tests(self, feature_id: UUID, test_ids: list[str]) -> list[dict]:
        return await self._request(
            "POST", f"/api/v1/features/{feature_id}/tests/approve",
            json={"test_ids": test_ids, "approved": True},
        )

    async def generate_code(self, feature_id: UUID, target_branch: str = "main") -> dict:
        return await self._request(
            "POST", f"/api/v1/features/{feature_id}/code/generate",
            json={"target_branch": target_branch},
        )

    async def push_to_github(self, feature_id: UUID, target_branch: str = "main") -> dict:
        return await self._request(
            "POST", f"/api/v1/features/{feature_id}/github/push",
            json={"target_branch": target_branch},
        )

    async def deploy_local(self, feature_id: UUID, target: str = "both") -> dict:
        return await self._request(
            "POST", f"/api/v1/features/{feature_id}/deploy/local",
            json={"target": target},
        )

    async def create_change_request(self, feature_id: UUID, title: str, description: str) -> dict:
        return await self._request(
            "POST", f"/api/v1/features/{feature_id}/change-request",
            json={"title": title, "description": description},
        )

    async def get_traceability(self, feature_id: UUID) -> dict:
        return await self._request("GET", f"/api/v1/features/{feature_id}/traceability")

    # --- GitHub ---
    async def connect_github(self, product_id: UUID, owner: str, repo_name: str) -> dict:
        return await self._request(
            "POST", f"/api/v1/github/connect/{product_id}",
            json={"owner": owner, "repo_name": repo_name},
        )


api_client = BackendAPIClient()
