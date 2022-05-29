from app.core.settings import PHONES_REGISTRY_URL
from app.repositories.database.mongo import MongoRepository
from app.repositories.phones_registry.digital_gov_ru import DigitalGovRu
from app.repositories.region_info.positionstack_repository import PositionStack
from app.services.update_phone_registry import UpdatePhoneRegistry


async def update_data():
	"""
	Обновление базы телефонных номеров.
	"""
	region_info_repository = PositionStack()
	registry_repository = DigitalGovRu(region_info_repository)

	db = MongoRepository()

	service = UpdatePhoneRegistry(registry_repository, db)

	await service.process_data(PHONES_REGISTRY_URL)
