from fastapi import APIRouter

from backend.app.api.v1.endpoints.features.post import router as post_router
from backend.app.api.v1.endpoints.features.get import router as get_router

router = APIRouter(prefix="/features", tags=["Features"])
router.include_router(post_router)
router.include_router(get_router)
