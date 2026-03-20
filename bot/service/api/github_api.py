"""GitHub API client — GitHub integration operations.

## Трассируемость
Feature: F014 — GitHub Integration
"""
from uuid import UUID

import httpx

from bot.core.config import bot_settings


class GitHubAPI:
    def __init__(self):
        self.base_url = bot_settings.backend_url.rstrip("/")

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30.0) as client:
            response = await client.request(method, path, **kwargs)
            response.raise_for_status()
            return response.json()

    async def connect_github(
        self, product_id: UUID | str, owner: str, repo_name: str
    ) -> dict:
        return await self._request(
            "POST",
            f"/api/v1/github/connect/{product_id}",
            json={"owner": owner, "repo_name": repo_name},
        )
