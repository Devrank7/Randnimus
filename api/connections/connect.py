from datetime import datetime, timedelta

from aiogram.types import Message, User
from apscheduler.triggers.date import DateTrigger

from api.keyboards.buttons import disconnect_buttons
from db.sql.model import Users
from db.sql.service import FindConnectionByConditionOrCreate, run_sql, ConnectConnection, ReadConnection, ReadUser
from scheduler.scheduler import scheduler
from scheduler.task import Disconnect
from .utils import prepare_id, get_info


class Connector:

    def __init__(self, message: Message, user: Users):
        self.message = message
        self.user = user

    async def connect(self):
        connect, full = await run_sql(FindConnectionByConditionOrCreate(self.message.from_user.id))
        if full:
            await run_sql(ConnectConnection(self.message.from_user.id))
        connect, first_user_id, second_user_id = await run_sql(ReadConnection(self.message.from_user.id))
        if first_user_id != -1 and second_user_id != -1:
            consumer = prepare_id(self.message, first_user_id, second_user_id)['consumer']
            user_consumer: Users = await run_sql(ReadUser(consumer))
            await self.message.answer(
                f"Вы были связанны с другим пользователем \n"
                f" {get_info(user_consumer, self.user.is_vip)} \n ⬇️ЧАТ НАЧАТ⬇️",
                reply_markup=disconnect_buttons)
            await self.message.bot.send_message(consumer,
                                                f"Вы были связаны!!! \n {get_info(self.user, user_consumer.is_vip)}"
                                                f" \n ⬇️ЧАТ НАЧАТ⬇️",
                                                reply_markup=disconnect_buttons)
            task = Disconnect(self.message.bot, connect.id)
            scheduler.add_job(func=task.run, trigger=DateTrigger(run_date=datetime.now() + timedelta(minutes=2)),
                              id=f"connect_{connect.id}")
        else:
            await self.message.answer("Ожидаем другого пользователя! ⌛", reply_markup=disconnect_buttons)
