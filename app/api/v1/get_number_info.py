from fastapi import APIRouter, status, Depends

from app.api.dependencies.services import get_phone_info_service
from app.api.dtos.response_wrapper import ResponseWrapper
from app.domain.entities.phone_detail import PhoneDetail
from app.domain.entities.phone_number_for_info import PhoneNumberForInfo
from app.services.get_phone_info import AbstractGetPhoneInfo

router = APIRouter()


@router.get(
	"/get_number_info",
	status_code=status.HTTP_200_OK,
	response_model=ResponseWrapper[PhoneDetail],
	operation_id="getNumberInfo",
	description="Получение информации по номеру телефона"
)
async def get_info(
	phone: PhoneNumberForInfo = Depends(),
	service: AbstractGetPhoneInfo = Depends(get_phone_info_service)
) -> ResponseWrapper[PhoneDetail]:
	result = await service.get_info(phone.number)
	return ResponseWrapper[PhoneDetail].make_success(result)
