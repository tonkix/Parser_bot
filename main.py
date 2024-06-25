import time
import os
from datetime import datetime
import asyncio
import logging
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

from openpyxl import Workbook

from app.parser_1 import parsing
from app.db.models import async_main
from app.handlers import router
from app.scheduler import send_message_cron_at_start
from app.scheduler import SchedulerMiddleware

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(filename='logs.log',
                    format="%(levelname)s - %(asctime)s - %(funcName)s: %(lineno)d - %(message)s",
                    level=logging.INFO)


async def main():
    logging.info('---START---')
    await async_main()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    scheduler = AsyncIOScheduler()

    scheduler.add_job(send_message_cron_at_start, trigger='date',
                      run_date=datetime.now() + timedelta(seconds=1),
                      kwargs={'bot': bot})

    scheduler.start()
    dp.include_router(router)
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot disabled")
        logging.info('---Bot disabled---')
