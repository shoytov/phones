from abc import ABC, abstractmethod

from app.domain.entities.region_timezone import RegionTimezone


class AbstractRegionInfo(ABC):
	@abstractmethod
	async def get_timezone(self, region: str) -> RegionTimezone:
		raise NotImplementedError()
