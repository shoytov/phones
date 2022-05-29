from typing import Optional

from pydantic import BaseModel


class PagingOffset(BaseModel):
    offset: Optional[int] = 0
    limit: int = 10


class ResponsePagingOffset(PagingOffset):
    total: int = 0


class PagingByPage(BaseModel):
    page: Optional[int] = 1
    limit: int = 10


class ResponsePagingByPage(PagingByPage):
    total: int = 0


class RequestLimit(BaseModel):
    limit: Optional[int] = 10
