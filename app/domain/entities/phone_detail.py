from typing import Optional

from pydantic import BaseModel

from app.domain.entities.region_timezone import RegionTimezone


class PhoneDetail(BaseModel):
	"""
	Данные о телефонном номере, которые отображаются при запросе.
	"""
	country: str
	region: str
	provider: str
	timezone: Optional[RegionTimezone]
