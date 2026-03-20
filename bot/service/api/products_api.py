"""Products API client — product-level backend operations.

## Трассируемость
Feature: F001 — Product Creation & Discovery
"""
from uuid import UUID

import httpx

from bot.core.config import bot_settings


class ProductsAPI:
    def __init__(self):
        self.base_url = bot_settings.backend_url.rstrip("/")

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30.0) as client:
            response = await client.request(method, path, **kwargs)
            response.raise_for_status()
            return response.json()

    async def create_product(self, idea_text: str, name: str | None = None) -> dict:
        return await self._request(
            "POST", "/api/v1/products", json={"idea_text": idea_text, "name": name}
        )

    async def submit_discovery(
        self, product_id: UUID | str, question: str, answer: str
    ) -> dict:
        return await self._request(
            "POST",
            f"/api/v1/products/{product_id}/discovery",
            json={"question": question, "answer": answer},
        )

    async def generate_feature_map(self, product_id: UUID | str) -> list[dict]:
        return await self._request(
            "POST", f"/api/v1/products/{product_id}/features"
        )

    async def approve_feature_map(
        self, product_id: UUID | str, feature_ids: list[str]
    ) -> dict:
        return await self._request(
            "POST",
            f"/api/v1/products/{product_id}/features/approve",
            json={"feature_ids": feature_ids},
        )
