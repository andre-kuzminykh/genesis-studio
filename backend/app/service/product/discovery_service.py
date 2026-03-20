"""Discovery service — handles product creation and guided discovery interview.

## Трассируемость
Feature: F001 Product Creation & Discovery
Scenario: UC-1.1, UC-1.2
"""
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.model.enums import ProductStatus, FeatureStatus
from backend.app.model.feature import FeatureModel
from backend.app.model.product import ProductModel
from backend.app.repository.product import ProductRepository
from backend.app.repository.feature import FeatureRepository

# Discovery questions asked in sequence
DISCOVERY_QUESTIONS = [
    "Who are the target users of this product?",
    "What is the main problem this product solves?",
    "What are the key goals or outcomes you want to achieve?",
    "What client types should be supported (Telegram bot, web, API)?",
    "Are there any technical constraints or preferences (hosting, integrations, etc.)?",
    "What are the 3-5 most important features you envision?",
]


class DiscoveryService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.product_repo = ProductRepository(session)
        self.feature_repo = FeatureRepository(session)

    async def create_product(
        self, idea_text: str, name: str | None = None, constraints: dict | None = None
    ) -> dict:
        """Create a new product from an idea and start discovery."""
        product = await self.product_repo.create(idea_text=idea_text, name=name, constraints=constraints)
        product = await self.product_repo.update_status(product, ProductStatus.discovery_in_progress)
        await self.session.commit()

        return {
            "product": product,
            "follow_up_questions": DISCOVERY_QUESTIONS[:3],
            "is_complete": False,
        }

    async def submit_discovery_answer(
        self, product_id: uuid.UUID, question: str, answer: str
    ) -> dict:
        """Submit an answer to a discovery question and get next questions."""
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")

        # Count existing responses to determine step
        step_number = len(product.interview_responses)
        await self.product_repo.add_interview_response(product_id, question, answer, step_number)

        # Extract product brief from accumulated answers
        responses_count = step_number + 1
        is_complete = responses_count >= len(DISCOVERY_QUESTIONS)

        if is_complete:
            # Auto-extract product summary from answers
            product = await self.product_repo.update(
                product,
                summary=f"Product based on: {product.idea_text}",
                status=ProductStatus.feature_map_draft,
            )

        next_questions = []
        if not is_complete:
            start_idx = min(responses_count, len(DISCOVERY_QUESTIONS))
            next_questions = DISCOVERY_QUESTIONS[start_idx : start_idx + 2]

        await self.session.commit()

        return {
            "product": product,
            "follow_up_questions": next_questions,
            "is_complete": is_complete,
        }

    async def generate_feature_map(self, product_id: uuid.UUID) -> list:
        """Generate initial feature map from discovery data."""
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")

        # Generate initial feature map based on discovery data
        # In production, this would call LLM to analyze discovery answers
        initial_features = [
            {"feature_id": "F001", "name": "Core Functionality", "overview": "Main business logic and data processing"},
            {"feature_id": "F002", "name": "User Management", "overview": "Authentication and user profile management"},
            {"feature_id": "F003", "name": "API Integration", "overview": "External service integrations"},
        ]

        features = await self.feature_repo.bulk_create(product_id, initial_features)
        await self.session.commit()
        return features

    async def approve_feature_map(self, product_id: uuid.UUID, feature_ids: list[uuid.UUID]) -> dict:
        """Approve the feature map for a product."""
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")

        product = await self.product_repo.update_status(product, ProductStatus.feature_map_approved)
        features = await self.feature_repo.list_by_product(product_id)
        await self.session.commit()

        return {"product": product, "features": features, "is_approved": True}
