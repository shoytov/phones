from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.phone_registry_record import PhoneRegistryRecord
from app.repositories.database.base import AbstractDatabase
from app.repositories.phones_registry.base import AbstractPhonesRegistry
import threading


class AbstractUpdatePhoneRegistry(ABC):
	def __init__(self, phone_repository: AbstractPhonesRegistry, db: AbstractDatabase):
		self.phone_repository = phone_repository
		self.db = db

	@abstractmethod
	async def process_data(self):
		"""
		Получение данных записей реестра для последующего сохранения в бд.
		"""
		raise NotImplementedError()

	@abstractmethod
	async def save_data(self, data: PhoneRegistryRecord):
		"""
		Сохранение данных реестра в БД.
		"""
		raise NotImplementedError()


class UpdatePhoneRegistry(AbstractUpdatePhoneRegistry):
	async def process_data(self, url: Optional[str] = None):
		files = await self.phone_repository.get_links_for_parse(url)
		for _ in range(len(files)):
			t = threading.Thread(target=make_transactions, name="WalletTest")

		# async for record in self.phone_repository.parse_data(url):  # type: ignore
		# 	await self.save_data(record)

	async def save_data(self, data: PhoneRegistryRecord):
		await self.db.insert_or_update_registry_record(data)
