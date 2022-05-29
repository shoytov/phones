from typing import Optional

from pydantic import BaseModel


class RegionTimezone(BaseModel):
	"""
	Поля таймзоны региона.
	"""
	name: Optional[str] = None  # название таймзоны
	offset_string: Optional[str] = None  # смещение относительно UTC
