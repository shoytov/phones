import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.tasks import update_data
from app.utils.init_cache import init_cache_redis


async def init_scheduler() -> AsyncIOScheduler:
	init_cache_redis()
	scheduler = AsyncIOScheduler(timezone="UTC")

	scheduler.add_job(
		update_data,
		trigger="cron",
		hour=8,
		minute=54
	)
	scheduler.start()

	return scheduler


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	asyncio.ensure_future(init_scheduler())
	loop.run_forever()
