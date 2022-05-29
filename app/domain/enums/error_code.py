from enum import Enum


class ErrorCode(str, Enum):
    BASE_ERROR_CODE = "BASE_ERROR_CODE"
    SERVER_ERROR = "SERVER_ERROR"
    ITEM_NOT_FOUND = "ITEM_NOT_FOUND"
    INVALID_FILTER_ITEM = "INVALID_FILTER_ITEM"
    REMOTE_SERVER_ERROR = "REMOTE_SERVER_ERROR"
    CONNECTION_ERROR = "CONNECTION_ERROR"
    BUSINESS_ERROR_CODE = "BUSINESS_ERROR_CODE"
    INVALID_FIELD_VALUE = "INVALID_FIELD_VALUE"
    UNAUTHORIZED = "UNAUTHORIZED"
    ENTITY_ALREADY_EXISTS = 'ENTITY_ALREADY_EXISTS'
    UNKNOWN = "UNKNOWN"

    @staticmethod
    def from_str(code: str) -> "ErrorCode":
        if not code:
            return ErrorCode.UNKNOWN
        elif code in ErrorCode._member_names_:
            return ErrorCode[code]
        else:
            return ErrorCode.BASE_ERROR_CODE
