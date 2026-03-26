from fastapi import APIRouter
from core.config import settings

router = APIRouter(tags=["Info"])


@router.get("/api/info")
async def app_info():
    return {
        "app_name": settings.app_name,
        "debug": settings.debug,
        "api_v1_prefix": settings.api_v1_prefix,
        "log_level": settings.log_level
    }