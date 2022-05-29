from app.api.dtos.error_wrapper import ErrorWrapper
from app.api.dtos.response_wrapper import ResponseWrapper
from app.api.handlers.validation_error_handler import _build_response
from app.domain.enums.error_code import ErrorCode
from app.domain.enums.error_type import ErrorType
from starlette.requests import Request
from starlette.responses import Response


def auth_exception_handler(request: Request, exc: Exception) -> Response:
    error_wrapper = ResponseWrapper[None]().make_error(
        error=ErrorWrapper(
            type=ErrorType.BASE,
            code=ErrorCode.UNAUTHORIZED,
            msg=exc.args[0] if exc.args and exc.args[0] else "Invalid credentials",
        )
    )
    return _build_response(content=error_wrapper.json(), status_code=401)
