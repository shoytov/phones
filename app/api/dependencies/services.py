from fastapi import Depends

from app.repositories.database.base import AbstractDatabase
from app.services.get_phone_info import GetPhoneInfo
from .repositories import get_mongodb_repository


def get_phone_info_service(db: AbstractDatabase = Depends(get_mongodb_repository)) -> GetPhoneInfo:
	service = GetPhoneInfo(db)
	return service
