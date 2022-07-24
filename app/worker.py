import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.tasks import update_data


async def init_scheduler() -> AsyncIOScheduler:
	scheduler = AsyncIOScheduler(timezone="UTC")

	scheduler.add_job(
		update_data,
		trigger="cron",
		hour=18,
		minute=30
	)
	scheduler.start()

	return scheduler


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	asyncio.ensure_future(init_scheduler())
	loop.run_forever()
