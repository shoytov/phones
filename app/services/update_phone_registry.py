import asyncio
from abc import ABC, abstractmethod
from multiprocessing import Process
from typing import Optional

from app.repositories.database.base import AbstractDatabase
from app.repositories.phones_registry.base import AbstractPhonesRegistry
from app.utils.init_cache import init_cache_redis
from app.utils.init_db import connect_db


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
	async def process_file(self, filename: str) -> None:
		"""
		Сохранение данных реестра в БД.
		"""
		raise NotImplementedError()


class UpdatePhoneRegistry(AbstractUpdatePhoneRegistry):
	def _process_record(self, filename: str):
		"""
		Инициализируем среду для обработки срок из файла.
		"""
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		init_cache_redis()
		connect_db(loop)
		loop.run_until_complete(self.process_file(filename))

	async def process_data(self, url: Optional[str] = None):
		"""
		Запуск процесса обработки. Точка входа.
		"""
		# получаем список ссылок для скачивания
		links = await self.phone_repository.get_links_for_parse(url)

		# качаем файлы и формируем массив файлов для обработки
		files = []
		for link in links:
			file_name = await self.phone_repository.download_file(link)
			files.append(file_name)

		# запускаем каждый файл для обработки в своем процессе
		for file in files:
			p = Process(target=self._process_record, args=(file,))
			p.start()

	async def process_file(self, filename: str):
		async for processed_records in self.phone_repository.process_file(filename):  # type: ignore
			await self.db.insert_or_update_registry_record(processed_records)
