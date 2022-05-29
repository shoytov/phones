from app.domain.enums.error_code import ErrorCode
from app.domain.enums.error_type import ErrorType
from app.domain.exceptions.base_exception import BaseDomainException


class ExternalServiceException(BaseDomainException):
    def __init__(
        self,
        msg: str = "",
        error_type: ErrorType = ErrorType.EXTERNAL_CONNECTIONS,
        code: ErrorCode = ErrorCode.REMOTE_SERVER_ERROR,
    ):
        self.type = error_type
        self.code = code
        self.msg = msg
