from typing import Any, Dict, Optional

from app.domain.enums.error_code import ErrorCode
from app.domain.enums.error_type import ErrorType
from pydantic import BaseModel


class ErrorWrapper(BaseModel):
    type: ErrorType = ErrorType.BASE  # noqa: A003
    code: ErrorCode = ErrorCode.SERVER_ERROR
    msg: Optional[str]
    context: Optional[Any]
    params: Optional[Dict[str, str]]
