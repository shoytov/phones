from abc import ABC, abstractmethod
from typing import Tuple

from app.domain.entities.phone_detail import PhoneDetail
from app.domain.entities.phone_registry_record import PhoneRegistryRecord


class AbstractDatabase(ABC):
	@abstractmethod
	async def insert_or_update_registry_record(self, data: PhoneRegistryRecord):
		"""
		Добавление/обновление записи в реестре.
		"""
		raise NotImplementedError()

	@abstractmethod
	async def get_number_info(self, number_parts: Tuple[str, str, str]) -> PhoneDetail:
		raise NotImplementedError()
