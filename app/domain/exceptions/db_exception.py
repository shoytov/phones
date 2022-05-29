from app.domain.enums.error_code import ErrorCode
from app.domain.enums.error_type import ErrorType
from app.domain.exceptions.base_exception import BaseDomainException


class DbException(BaseDomainException):
    def __init__(
        self,
        msg: str = "",
        error_type: ErrorType = ErrorType.DATABASES,
        code: ErrorCode = ErrorCode.BASE_ERROR_CODE,
    ):
        self.type = error_type
        self.code = code
        self.msg = msg
