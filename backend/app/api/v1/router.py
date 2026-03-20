"""API v1 router — aggregates all endpoint routers."""
from fastapi import APIRouter

from backend.app.api.v1.products import router as products_router
from backend.app.api.v1.features import router as features_router
from backend.app.api.v1.github import router as github_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(products_router)
api_v1_router.include_router(features_router)
api_v1_router.include_router(github_router)
