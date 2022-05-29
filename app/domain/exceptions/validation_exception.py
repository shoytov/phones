from app.domain.enums.error_code import ErrorCode
from app.domain.enums.error_type import ErrorType
from app.domain.exceptions.base_exception import BaseDomainException


class ValidationException(BaseDomainException):
    def __init__(
        self,
        msg: str = "",
        error_type: ErrorType = ErrorType.VALIDATION,
        code: ErrorCode = ErrorCode.BASE_ERROR_CODE,
        context: str = "",
        status_code: int = 400,

    ):
        super().__init__()
        
        self.type = error_type
        self.code = code
        self.msg = msg
        self.http_status = status_code
        
        if context:
            self.context = context
