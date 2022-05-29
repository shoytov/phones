from app.api.dtos.error_wrapper import ErrorWrapper
from app.api.dtos.response_wrapper import ResponseWrapper
from app.api.handlers.validation_error_handler import _build_response
from app.core.settings.base import DEBUG
from app.domain.exceptions.base_exception import BaseDomainException
from fastapi import status
from starlette.responses import Response


async def business_exception_handler(request, exc: BaseDomainException) -> Response:
    if DEBUG:
        error_wrapper = ResponseWrapper[None].make_error(
            error=ErrorWrapper(
                type=exc.type,
                code=exc.code,
                msg=exc.msg if exc.msg else "Ошибка сервера",
                context=exc.context,
            )
        )
    else:
        error_wrapper = ResponseWrapper[None].make_error(
            error=ErrorWrapper(
                type=exc.type,
                code=exc.code,
                msg=exc.msg if exc.msg else "Ошибка сервера",
            )
        )

    http_status = exc.http_status if exc.http_status else status.HTTP_400_BAD_REQUEST

    return _build_response(
        content=error_wrapper.json(),
        status_code=http_status if exc else status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
