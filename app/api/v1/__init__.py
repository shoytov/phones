from fastapi import APIRouter

from .get_number_info import router as get_number_info_router

router = APIRouter()

router.include_router(get_number_info_router, prefix="", tags=["v1"])
