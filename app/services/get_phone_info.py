from abc import ABC, abstractmethod

from app.domain.entities.phone_detail import PhoneDetail
from app.repositories.database.base import AbstractDatabase
from app.utils.parse_number import ParseNumberFactory


class AbstractGetPhoneInfo(ABC):
	def __init__(self, db: AbstractDatabase):
		self.db = db

	@abstractmethod
	async def get_info(self, number: str) -> PhoneDetail:
		raise NotImplementedError()


class GetPhoneInfo(AbstractGetPhoneInfo):
	async def get_info(self, number: str) -> PhoneDetail:
		factory = ParseNumberFactory(number)
		code, prefix, tail = await factory.call_parser_method()

		return await self.db.get_number_info((code, prefix, tail))
