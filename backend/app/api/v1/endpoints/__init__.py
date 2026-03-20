from backend.app.api.v1.endpoints.products import router as products_router
from backend.app.api.v1.endpoints.features import router as features_router
from backend.app.api.v1.endpoints.github import router as github_router

__all__ = ["products_router", "features_router", "github_router"]
