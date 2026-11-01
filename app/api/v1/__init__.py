from fastapi import APIRouter

from app.api.v1.endpoints import health, tasks

router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(tasks.router, tags=["tasks"])
