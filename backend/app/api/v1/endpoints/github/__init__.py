from fastapi import APIRouter

from backend.app.api.v1.endpoints.github.post import router as post_router

router = APIRouter(prefix="/github", tags=["GitHub"])
router.include_router(post_router)
