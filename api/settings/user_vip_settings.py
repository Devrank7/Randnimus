import os
from datetime import timedelta, datetime

from aiogram.types import Message, LabeledPrice
from apscheduler.triggers.date import DateTrigger
from dotenv import load_dotenv

from db.sql.service import run_sql, UpdateUser
from scheduler.scheduler import scheduler
from scheduler.task import TakeOutVIP

load_dotenv()
PROVIDER_TOKEN = os.getenv('PAYMENT_KEY')


async def prepare_invoice(message: Message):
    await message.answer_invoice(
        title=f"VIP на 7 дней!",
        description="Вы сможете видеть данные пользователя при общении, Имя, Возраст, Пол!!!",
        payload="invoice",
        currency="USD",
        prices=[LabeledPrice(amount=1000, label="VIP")],
        provider_token=PROVIDER_TOKEN,
    )


async def give_vip_on(message: Message, on_days: int):
    until = datetime.now() + timedelta(days=on_days)
    await run_sql(UpdateUser(message.from_user.id, is_vip=True))
    task = TakeOutVIP(message.bot, message.from_user.id)
    scheduler.add_job(task.run, DateTrigger(run_date=until))
    await message.answer("Вы получили VIP не неделю. Спасибо за покупку!!!")
