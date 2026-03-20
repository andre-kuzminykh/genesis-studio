from fastapi import APIRouter

from backend.app.api.v1.endpoints.products.post import router as post_router

router = APIRouter(prefix="/products", tags=["Products"])
router.include_router(post_router)
