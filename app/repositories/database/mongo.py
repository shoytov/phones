import asyncio
from typing import Tuple

import pymongo
from motor import motor_asyncio

from app.core.settings import (
	MONGODB_HOST,
	MONGODB_PORT,
	MONGODB_USER,
	MONGODB_PASSWORD,
	MONGODB_DB,
	MONGO_DB_PHONES_REGISTRY_COLLECTION
)
from app.domain.entities.phone_detail import PhoneDetail
from app.domain.entities.phone_registry_record import PhoneRegistryRecord
from app.domain.enums.error_code import ErrorCode
from app.domain.exceptions.business_exception import BusinessException
from .base import AbstractDatabase

loop = asyncio.get_event_loop()


class MongoRepository(AbstractDatabase):
	def __init__(self):
		global loop

		self.client = motor_asyncio.AsyncIOMotorClient(self.connection_string, io_loop=loop)
		self.db = self.client[MONGODB_DB]

		# создаем индексы
		collection = self.db[MONGO_DB_PHONES_REGISTRY_COLLECTION]
		collection.create_index(
			[
				("code", pymongo.ASCENDING),
				("digit_range.from_", pymongo.ASCENDING),
				("digit_range.to_", pymongo.ASCENDING)
			],
			unique=True
		)

	@property
	def connection_string(self) -> str:
		if MONGODB_USER and MONGODB_PASSWORD:
			_connection_string = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}"
		else:
			_connection_string = f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}"

		return _connection_string

	@connection_string.setter
	def connection_string(self, value: str):
		pass

	async def get_number_info(self, number_parts: Tuple[str, str, str]) -> PhoneDetail:
		collection = self.db[MONGO_DB_PHONES_REGISTRY_COLLECTION]

		condition = {
			"code": number_parts[0],
			"prefix": number_parts[1],
			"digit_range.from_": {
				"$lte": int(number_parts[2])
			},
			"digit_range.to_": {
				"$gte": int(number_parts[2])
			}
		}

		res = await collection.find_one(condition)

		if res:
			return PhoneDetail(
					country=res.get("country"),
					region=res.get("region"),
					provider=res.get("provider"),
					timezone=res.get("timezone")
			)
		raise BusinessException(
				msg="Номер не найден в базе",
				code=ErrorCode.ITEM_NOT_FOUND
		)

	async def insert_or_update_registry_record(self, data: PhoneRegistryRecord):
		collection = self.db[MONGO_DB_PHONES_REGISTRY_COLLECTION]

		condition = {
			"code": data.code,
			"digit_range": {
				"from_": data.digit_range.from_,
				"to_": data.digit_range.to_
			}

		}
		data = data.dict()

		# убираем обновление таймзоны, если получены пустые значения
		if data.get("timezone") is None or data.get("timezone").get("name") is None \
				or data.get("timezone").get("offset_string") is None:
			del data["timezone"]

		await collection.update_one(condition, {"$set": data}, upsert=True)
