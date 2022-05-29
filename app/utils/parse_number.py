from typing import Tuple

from app.domain.enums.error_code import ErrorCode
from app.domain.exceptions.validation_exception import ValidationException


class ParseNumber:
	def __init__(self, number: str):
		self.number = number

	async def parse_ru_number(self) -> Tuple[str, str, str]:
		"""
		Разбиение номера РФ на 3 составляющие: код, префикс, остальная часть.
		"""
		if len(self.number) != 12:
			raise ValidationException(
					msg="В номере РФ должно быть 12 символов, включая +",
					code=ErrorCode.INVALID_FIELD_VALUE
			)

		return self.number[0:2], self.number[2:5], self.number[5:]


class ParseNumberFactory:
	"""
	Фабрика для вызова метода разбиения телефонного номера на части в зависимости от код страны.
	"""
	def __init__(self, number: str):
		self.number = number
		self.parser = ParseNumber(number)

	async def call_parser_method(self) -> Tuple[str, str, str]:
		return {
			"+7": await self.parser.parse_ru_number()
		}.get(self.number[0:2])
