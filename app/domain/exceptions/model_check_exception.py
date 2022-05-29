from app.domain.enums.error_code import ErrorCode
from app.domain.enums.error_type import ErrorType
from app.domain.exceptions.base_exception import BaseDomainException


class ModelFieldValueException(BaseDomainException):
    def __init__(
        self,
        msg: str = "",
        error_type: ErrorType = ErrorType.MODELS,
        code: ErrorCode = ErrorCode.INVALID_FIELD_VALUE,
        context: str = "",
    ):
        super().__init__()
        self.type = error_type
        self.code = code
        self.msg = msg
        if context:
            self.context = context


class SortFieldValueException(BaseDomainException):
    def __init__(
        self,
        msg: str = "",
        error_type: ErrorType = ErrorType.MODELS,
        code: ErrorCode = ErrorCode.INVALID_FIELD_VALUE,
        context: str = "",
    ):
        super().__init__()
        self.type = error_type
        self.code = code
        self.msg = msg
        if context:
            self.context = context
