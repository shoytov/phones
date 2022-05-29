from pydantic import BaseModel, validator

from app.domain.enums.error_code import ErrorCode
from app.domain.exceptions.validation_exception import ValidationException


class PhoneNumberForInfo(BaseModel):
	"""
	Сущность для запроса информации о телефонном номере.
	"""
	number: str

	@classmethod
	@validator("number")
	def check_number(cls, v: str):
		for i, symbol in enumerate(v):
			if i == 0 and symbol != "+":
				raise ValidationException(
						msg="Номер должен начинаться на +",
						code=ErrorCode.INVALID_FIELD_VALUE
				)
			else:
				try:
					int(symbol)
				except ValueError:
					raise ValidationException(
							msg="В номере присутствуют не только цифры и знак +",
							code=ErrorCode.INVALID_FIELD_VALUE
					)
