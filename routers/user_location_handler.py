from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

from api.settings.user_age_settings import change_age_markup
from db.sql.model import Users
from db.sql.service import run_sql, AttachLocation, ReadUser

router = Router()


@router.message(F.location)
async def location_handler(message: Message):
    location = message.location
    user: Users = await run_sql(ReadUser(message.from_user.id))
    await run_sql(AttachLocation(user.tg_id, location.latitude, location.longitude))
    await message.answer("Спасибо за локацию! Укажите свой возраст! 👱",
                         reply_markup=change_age_markup(0, 36, prefix="sage_", pag_prefix="spag_"))
    await message.answer("Нам нужен ваш возраст для нахождения партнеров! 👁️", reply_markup=ReplyKeyboardRemove())
