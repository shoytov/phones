import asyncio
from asyncio.events import AbstractEventLoop
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.settings import (
	MONGODB_HOST,
	MONGODB_PORT,
	MONGODB_USER,
	MONGODB_PASSWORD
)

db_client: AsyncIOMotorClient = None
loop = asyncio.get_event_loop()


def connection_string() -> str:
	if MONGODB_USER and MONGODB_PASSWORD:
		_connection_string = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}"
	else:
		_connection_string = f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}"

	return _connection_string


def get_db_client() -> AsyncIOMotorClient:
	global db_client
	return db_client


def connect_db(_loop: Optional[AbstractEventLoop] = None):
	global db_client

	if _loop is None:
		global loop
		_loop = loop

	db_client = AsyncIOMotorClient(connection_string(), io_loop=_loop)


async def close_db():
	global db_client
	db_client.close()
