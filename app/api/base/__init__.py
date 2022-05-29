"""
Системные эндпоинты, такие как проверка работоспособности сервиса и т.д.
"""
from fastapi import APIRouter

from .ping import router as ping_router

router = APIRouter()

router.include_router(ping_router, prefix="", tags=["system"])
