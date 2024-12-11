from aiogram.types import Message, CallbackQuery

from api.keyboards.buttons import button_chat
from api.keyboards.keyboard import EnumKeyboardMarkup
from api.settings.sex.util import translate
from db.sql.enum.enums import Sex
from db.sql.service import run_sql, UpdateUser


async def change_sex(message: Message, text: str = "Выберете пол 👀", prefix: str = "sex_"):
    markup = EnumKeyboardMarkup(Sex, prefix, name_func=lambda el: translate(el.value))
    await message.answer(text, reply_markup=markup.as_keyboard_markup())


async def change_query_sex(query: CallbackQuery):
    sex = query.data.split("_")[1]
    match sex.lower():
        case "male":
            await run_sql(UpdateUser(query.from_user.id, Sex.MALE))
            await query.answer("Male")
            await query.message.answer("Ваш пол изменен на мужской👳‍♂️")
        case "female":
            await run_sql(UpdateUser(query.from_user.id, Sex.FEMALE))
            await query.answer("Female")
            await query.message.answer("Ваш пол изменен на женский👩‍🦳")
        case "unknown":
            await run_sql(UpdateUser(query.from_user.id, Sex.UNKNOWN))
            await query.answer("Unknown")
            await query.message.answer("Ваш пол изменен на необозначенный🕵️")
        case _:
            await query.answer("Not found!", show_alert=True)


async def change_or_register(query: CallbackQuery):
    await change_query_sex(query)
    await query.message.delete()
    await query.message.answer("Вы успешно зарегистрировались💪", reply_markup=button_chat)
