import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

from app.db.models import async_main
from app.handlers import router
from app.scheduler import send_message_cron_at_start
from app.scheduler import SchedulerMiddleware

from aiogram.types import BotCommand, BotCommandScopeDefault

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def set_commands(bot: Bot):
    commands = [BotCommand(command='help',
                           description='Помощь'),
                BotCommand(command='user_settings_info',
                           description='Показать текущие настройки'),
                BotCommand(command='backup',
                           description='Выгрузка БД'),
                BotCommand(command='clear_log',
                           description='Очистить логи'),
                BotCommand(command='subscribe',
                           description='Подписаться на рассылку'),
                BotCommand(command='unsubscribe',
                           description='Отписаться от рассылки'),
                BotCommand(command='product_search',
                           description='Поиск товаров через сообщение'),
                BotCommand(command='writing_to_db',
                           description='Запись ссылок в БД'),
                BotCommand(command='creating_dictionary_worksheet',
                           description='Переключатель записи в Excel отдельного листа'),
                BotCommand(command='import',
                           description='Импорт товаров ТТ')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


logging.basicConfig(filename='logs.log',
                    format="%(levelname)s - %(asctime)s - %(funcName)s: %(lineno)d - %(message)s",
                    level=logging.INFO)


async def main():
    logging.info('[INFO] ---START---')
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
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[INFO] Bot disabled")
        logging.info('[INFO] ---Bot disabled---')
