from __future__ import annotations

from io import BytesIO
from typing import Generic, Optional, TypeVar

from app.api.dtos.error_wrapper import ErrorWrapper
from app.api.dtos.response_paging import ResponsePagingByPage
from app.domain.entities.paging import PagingResultEntity
from pydantic import Field
from pydantic.generics import GenericModel
from starlette.responses import StreamingResponse

ResponseWrapperDataT = TypeVar("ResponseWrapperDataT")


class ResponseWrapper(GenericModel, Generic[ResponseWrapperDataT]):
    """
    Cущность объекта возврата результата.
    """

    data: Optional[ResponseWrapperDataT] = Field(
        None, description="Результат запроса (основные данные)"
    )
    is_success: bool = Field(
        True, alias="isSuccess", description="Признак успешности выполнения запроса"
    )
    paging: Optional[ResponsePagingByPage] = Field(
        None, description="Объект пагинации (если предусмотрено запросом)"
    )
    error: Optional[ErrorWrapper] = Field(
        None,
        description=(
            "Объект содержащий данные об ошибках в случае неудачного выполнения запроса"
        ),
    )

    @staticmethod
    def make_success(
        data: Optional[ResponseWrapperDataT],
        paging: Optional[ResponsePagingByPage] = None,
    ) -> ResponseWrapper[ResponseWrapperDataT]:
        """
        Формирование ответа в JSON формате.
        """
        if isinstance(data, PagingResultEntity):
            return ResponseWrapper(
                data=data.data,
                paging=ResponsePagingByPage(
                    total=data.total,
                    page=data.page,
                    limit=data.limit,
                ),
                is_success=True,
            )
        return ResponseWrapper(data=data, paging=paging, is_success=True)

    @staticmethod
    def make_success_download(data: BytesIO, filename: str) -> StreamingResponse:
        """
        Отдача файла в респонс.
        """
        headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
        return StreamingResponse(content=data, headers=headers)

    @staticmethod
    def make_error(
        error: Optional[ErrorWrapper] = None,
    ) -> ResponseWrapper[ResponseWrapperDataT]:
        """
        Ошибки при неудачном ответе.
        """
        return ResponseWrapper(error=error, is_success=False)
