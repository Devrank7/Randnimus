import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from liqpay.liqpay import LiqPay

from db.sql.connect import init_db
from routers import start_router, settings_router, vip_router, chat_settings
from scheduler.scheduler import scheduler

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
routers = [
    start_router.router,
    settings_router.router,
    vip_router.router,
    chat_settings.router
]


@dp.startup()
async def start():
    print("Start bot!")


async def main():
    for router in routers:
        dp.include_router(router)
    await init_db()
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
