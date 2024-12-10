import abc
from abc import ABC

from aiogram import Bot

from db.sql.service import run_sql, UpdateUser, DeleteConnection, DeleteConnectionById


class Task(ABC):
    @abc.abstractmethod
    async def run(self):
        raise NotImplementedError


class Disconnect(Task):

    def __init__(self, bot: Bot, connection_id: int):
        self.bot = bot
        self.connection_id = connection_id

    async def run(self):
        connection = await run_sql(DeleteConnectionById(self.connection_id))
        text = "Соединение перервано!"
        await self.bot.send_message(connection.first_user_id, text)
        await self.bot.send_message(connection.second_user_id, text)


class TakeOutVIP(Task):

    def __init__(self, bot: Bot, user_tg_id: int):
        self.bot = bot
        self.user_tg_id = user_tg_id

    async def run(self):
        await run_sql(UpdateUser(tg_id=self.user_tg_id, is_vip=False))
        await self.bot.send_message(self.user_tg_id, "Я отобрал у вас VIP")
