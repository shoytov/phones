
from app.api.dtos.response_wrapper import ResponseWrapper
from app.domain.entities.paging import PagingResultEntity
from fastapi import APIRouter

router = APIRouter()


@router.get("/__ping__", description="Проверка контейнера сервиса")
async def pinger() -> ResponseWrapper:
    return ResponseWrapper[dict].make_success(
        data=PagingResultEntity[dict](data={"status": "ok"}, total=1, page=1, limit=10)  # type: ignore
    )
