import aioredis
from aioredis.client import Redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.core.settings import REDIS_URI


def get_redis_connection() -> Redis:
	redis = aioredis.from_url(
			REDIS_URI, encoding="utf8",
			decode_responses=True
	)
	return redis


def init_cache_redis() -> None:
	redis = get_redis_connection()
	FastAPICache.init(RedisBackend(redis), prefix="cache")
