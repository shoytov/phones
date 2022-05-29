from app.repositories.database.mongo import MongoRepository


def get_mongodb_repository() -> MongoRepository:
	repository = MongoRepository()
	return repository
