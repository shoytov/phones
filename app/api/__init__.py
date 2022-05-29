# Global REST API router
from fastapi import APIRouter

from .base import router as system_router
from .v1 import router as v1_router

base_router = APIRouter(prefix="")
router = APIRouter(prefix="/api")

router.include_router(v1_router, prefix="/v1")
base_router.include_router(system_router, prefix="")
