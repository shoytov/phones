from typing import Tuple

import pymongo

from app.core.settings import (
	MONGODB_DB,
	MONGO_DB_PHONES_REGISTRY_COLLECTION
)
from app.domain.entities.phone_detail import PhoneDetail
from app.domain.entities.phone_registry_record import PhoneRegistryRecord
from app.domain.enums.error_code import ErrorCode
from app.domain.exceptions.business_exception import BusinessException
from app.utils.init_db import get_db_client
from .base import AbstractDatabase


class MongoRepository(AbstractDatabase):
	def __init__(self):
		self.db = None

	async def set_db(self):
		db_client = get_db_client()
		self.db = db_client[MONGODB_DB]

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

	async def get_number_info(self, number_parts: Tuple[str, str, str]) -> PhoneDetail:
		await self.set_db()
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
		await self.set_db()
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
