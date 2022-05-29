from typing import Optional, TypeVar, Generic

from pydantic import BaseModel, constr, Field
from pydantic.generics import GenericModel

from .region_timezone import RegionTimezone

RangeT = TypeVar("RangeT")


class Range(GenericModel, Generic[RangeT]):
	from_: Optional[RangeT] = Field(...)
	to_: Optional[RangeT] = Field(...)


DigitRange = Range[int]


class PhoneRegistryRecord(BaseModel):
	"""
	Сущность элемента реестра телефонных номеров для записи в БД.
	"""
	code: str = "+7"
	prefix: constr(min_length=3, max_length=3)
	digit_range: DigitRange
	country: str = "Russia"
	region: str
	provider: str
	timezone: Optional[RegionTimezone]
