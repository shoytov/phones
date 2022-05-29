import sys
from typing import Optional

import app.core.settings.base as settings
from app.domain.enums.error_code import ErrorCode
from app.domain.enums.error_type import ErrorType


class BaseDomainException(Exception):
    type: ErrorType  # noqa: A003
    code: ErrorCode
    msg: str
    context: str = ""
    http_status: int = 200

    def __init__(
        self,
        msg: str = "",
        error_type: ErrorType = ErrorType.BASE,
        code: ErrorCode = ErrorCode.BASE_ERROR_CODE,
        http_status: Optional[int] = None,
    ):
        self.type = error_type
        self.code = code
        self.msg = msg

        if http_status:
            self.http_status = http_status

        if settings.DEBUG:
            self.context = str(sys.exc_info()[2])
