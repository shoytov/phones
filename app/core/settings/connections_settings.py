from starlette.config import Config

config = Config(".env")

PHONES_REGISTRY_URL: str = config.get("PHONES_REGISTRY_URL", cast=str)

MONGODB_HOST: str = config.get("MONGODB_HOST", cast=str)
MONGODB_PORT: int = config.get("MONGODB_PORT", cast=int)
MONGODB_USER: str = config.get("MONGODB_USER", cast=str)
MONGODB_PASSWORD: str = config.get("MONGODB_PASSWORD", cast=str)
MONGODB_DB: str = config.get("MONGODB_DB", cast=str)
MONGO_DB_PHONES_REGISTRY_COLLECTION: str = config.get("MONGO_DB_PHONES_REGISTRY_COLLECTION", cast=str)

REDIS_URI: str = config.get("REDIS_URI", cast=str)

# сервис получения данных о населенном пункте
POSITIONSTACK_BASE_URL: str = config.get("POSITIONSTACK_BASE_URL", cast=str)
POSITIONSTACK_APIKEY: str = config.get("POSITIONSTACK_APIKEY", cast=str)
