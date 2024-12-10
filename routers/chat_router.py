import datetime

from aiogram import Router, F
from aiogram.types import Message
from apscheduler.triggers.date import DateTrigger

from api.connections.connect import Connector
from api.connections.utils import prepare_id, check_and_notify_connect
from api.keyboards.buttons import button_chat
from db.sql.model import Connection, Users
from db.sql.service import run_sql, ReadConnection, DeleteConnection
from middlewares.middleware import AuthMiddleware
from scheduler.scheduler import scheduler

router = Router()
router.message.middleware(AuthMiddleware())


@router.message(F.text == "Начать чат")
async def chat_router(message: Message, user: Users):
    if await check_and_notify_connect(message):
        return
    connector = Connector(message, user)
    await connector.connect()


@router.message(F.text == "Отключится")
async def disconnect(message: Message):
    connect: Connection = await run_sql(DeleteConnection(message.from_user.id))
    if connect:
        job_id = f"connect_{connect.id}"
        if scheduler.get_job(job_id=job_id):
            scheduler.remove_job(job_id=job_id)
        await message.answer("Вы успешно отключились!", reply_markup=button_chat)
        connect_data = prepare_id(message, connect.first_user_id, connect.second_user_id)
        consumer = connect_data['consumer']
        if consumer != -1:
            await message.bot.send_message(consumer, "Пользователь отключился от вас!",
                                           reply_markup=button_chat)
        return
    await message.answer("Вы итак были отключены!", reply_markup=button_chat)


@router.message(F.text)
async def bot_reader_connect(message: Message):
    connect, first_user_id, second_user_id = await run_sql(ReadConnection(message.from_user.id))
    if first_user_id != -1 and second_user_id != -1:
        scheduler.reschedule_job(job_id=f"connect_{connect.id}",
                                 trigger=DateTrigger(run_date=datetime.datetime.now() + datetime.timedelta(minutes=2)))
        prepare_dict = prepare_id(message, first_user_id, second_user_id)
        await message.bot.send_message(prepare_dict['consumer'], f"Аноним: {message.text}")
    else:
        print("Connect not found!")
