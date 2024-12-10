import datetime

from aiogram import Router, F
from aiogram.types import Message
from apscheduler.triggers.date import DateTrigger

from api.connections.connect import Connector
from api.connections.utils import prepare_id, check_and_notify_connect
from db.sql.service import run_sql, ReadConnection, DeleteConnection
from middlewares.middleware import AuthMiddleware
from scheduler.scheduler import scheduler

router = Router()
router.message.middleware(AuthMiddleware())


@router.message(F.text == "Начать чат")
async def chat_router(message: Message):
    if await check_and_notify_connect(message):
        return
    connector = Connector(message)
    await connector.connect()


@router.message(F.text == "Отключится")
async def disconnect(message: Message):
    connect = await run_sql(DeleteConnection(message.from_user.id))
    if connect:
        scheduler.remove_job(job_id=f"connect_{connect.id}")
        await message.answer("Вы успешно отключились!")
        return
    await message.answer("Вы итак были отключены!")


@router.message(F.text)
async def bot_reader_connect(message: Message):
    connect, first_user_id, second_user_id = await run_sql(ReadConnection(message.from_user.id))
    if first_user_id and second_user_id:
        scheduler.reschedule_job(job_id=f"connect_{connect.id}",
                                 trigger=DateTrigger(run_date=datetime.datetime.now() + datetime.timedelta(minutes=20)))
        prepare_dict = prepare_id(message, first_user_id, second_user_id)
        await message.bot.send_message(prepare_dict['consumer'], f"Аноним: {message.text}")
    else:
        print("Connect not found!")
