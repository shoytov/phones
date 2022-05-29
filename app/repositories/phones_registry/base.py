from abc import ABC, abstractmethod
from typing import Optional, List

from app.repositories.region_info.base import AbstractRegionInfo


class AbstractPhonesRegistry(ABC):
	def __init__(self, region_info_repository: AbstractRegionInfo):
		# репозиторий определения часового пояса региона
		self.region_info_repository = region_info_repository

	@abstractmethod
	async def process_file(self, filename: str):
		"""
		Генератор, который отдает сформированную запись реестра.
		"""
		raise NotImplementedError()

	@abstractmethod
	async def get_links_for_parse(self, url: Optional[str] = None) -> List[str]:
		"""
		Получение данных для дальнейшего парсинга.
		Возвращает список ссылок на файлы, которые содержат данные регистра.
		"""
		raise NotImplementedError()

	@abstractmethod
	async def download_file(self, link: str) -> str:
		"""
		Сохраняет файл, и возвращает имя файла.
		"""
		raise NotImplementedError()
