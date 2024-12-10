from datetime import datetime, timedelta

from aiogram.types import Message
from apscheduler.triggers.date import DateTrigger

from api.keyboards.buttons import disconnect_buttons
from db.sql.service import FindHalfConnectionOrCreate, run_sql, ConnectConnection, ReadConnection
from scheduler.scheduler import scheduler
from scheduler.task import Disconnect
from .utils import prepare_id


class Connector:

    def __init__(self, message: Message):
        self.message = message

    async def connect(self):
        connect, full = await run_sql(FindHalfConnectionOrCreate(self.message.from_user.id))
        if full:
            await run_sql(ConnectConnection(self.message.from_user.id))
        connect, first_user_id, second_user_id = await run_sql(ReadConnection(self.message.from_user.id))
        if first_user_id != -1 and second_user_id != -1:
            await self.message.answer("Вы были связанны с другим пользователем!", reply_markup=disconnect_buttons)
            consumer = prepare_id(self.message, first_user_id, second_user_id)['consumer']
            await self.message.bot.send_message(consumer, "Вы были связаны!!!")
            task = Disconnect(self.message.bot, connect.id)
            scheduler.add_job(func=task.run, trigger=DateTrigger(run_date=datetime.now() + timedelta(minutes=20)),
                              job_id=f"connect_{connect.id}")
        else:
            await self.message.answer("Ожидаем другого пользователя!", reply_markup=disconnect_buttons)
