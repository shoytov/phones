from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

PagingEntityDataT = TypeVar("PagingEntityDataT")


class PagingEntity(BaseModel):
    page: int = 1
    limit: int = 10

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


class PagingResultEntity(GenericModel, Generic[PagingEntityDataT], PagingEntity):
    data: Optional[PagingEntityDataT] = Field(
        None, description="Результат запроса (основные данные)"
    )
    total: int = 0
