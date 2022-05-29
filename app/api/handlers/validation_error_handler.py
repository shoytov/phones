from typing import Any

from app.api.dtos.error_wrapper import ErrorCode, ErrorType, ErrorWrapper
from app.api.dtos.response_wrapper import ResponseWrapper
from app.core.settings import DEBUG
from fastapi import status
from fastapi.exceptions import RequestValidationError
from starlette.responses import Response


def _build_response(
    content: str, status_code: int = status.HTTP_200_OK, media_type: str = "application/json"
) -> Response:
    return Response(status_code=status_code, content=content, media_type=media_type)


async def validation_exception_handler(
    request: Any, exc: RequestValidationError
) -> Response:
    error_wrapper = ResponseWrapper[None].make_error(
        error=ErrorWrapper(
            type=ErrorType.VALIDATION,
            code=ErrorCode.INVALID_FILTER_ITEM,
            msg="Ошибка валидации",
            context=exc.errors() if DEBUG else None,
        )
    )
    return _build_response(
        content=error_wrapper.json(), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
