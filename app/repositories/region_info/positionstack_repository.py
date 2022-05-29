import requests
from fastapi_cache.decorator import cache
from requests.exceptions import ConnectionError, ConnectTimeout, HTTPError

from app.core.logging import app_logger
from app.core.settings import (
	POSITIONSTACK_BASE_URL,
	POSITIONSTACK_APIKEY
)
from app.domain.entities.region_timezone import RegionTimezone
from app.utils.cache_key_builder import key_builder
from app.utils.transliterate_text import translit_text
from .base import AbstractRegionInfo


class PositionStack(AbstractRegionInfo):
	@cache(key_builder=key_builder)
	async def get_timezone(self, region: str) -> RegionTimezone:
		region = await translit_text(region)

		try:
			response = requests.get(
				f"{POSITIONSTACK_BASE_URL}forward?access_key={POSITIONSTACK_APIKEY}&query={region}&timezone_module=1&limit=1"
			)
		except (ConnectionError, ConnectTimeout, HTTPError):
			app_logger.error(f"Сервис определения таймзоны недоступен. Ошибка произошла на регионе: {region}")
		else:
			if response.status_code == 200:
				data = response.json()

				try:
					return RegionTimezone(
						name=data.get("data")[0].get("timezone_module").get("name"),
						offset_string=data.get("data")[0].get("timezone_module").get("offset_string"),
					)
				except AttributeError:
					app_logger.error(f"Некорректные данные от сервиса: {data}")
					return RegionTimezone()
				except IndexError:
					app_logger.warning(f"Не найден регион: {region}")
					return RegionTimezone()

			app_logger.error(f"Неожиданный от сервиса определения таймзоны, {response.status_code}")
