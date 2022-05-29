from abc import ABC, abstractmethod
from typing import Optional, List

from app.repositories.region_info.base import AbstractRegionInfo


class AbstractPhonesRegistry(ABC):
	def __init__(self, region_info_repository: AbstractRegionInfo):
		# репозиторий определения часового пояса региона
		self.region_info_repository = region_info_repository

	@abstractmethod
	async def parse_data(self, url: Optional[str] = None):
		"""
		Обработка данных, точка входа.
		"""
		raise NotImplementedError()

	@abstractmethod
	async def get_links_for_parse(self, url: Optional[str] = None) -> List[str]:
		raise NotImplementedError()
