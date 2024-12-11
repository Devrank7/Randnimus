from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery

from api.keyboards.buttons import settings_button
from api.settings.user_age_settings import change_age_markup
from api.settings.user_sex_settings import change_sex, change_query_sex
from api.settings.user_vip_settings import prepare_invoice
from db.sql.model import Users
from db.sql.service import run_sql, UpdateUser
from middlewares.middleware import AuthMiddleware

router = Router()
router.message.middleware(AuthMiddleware())


@router.message(F.text == 'Настройки')
async def router_message(message: Message):
    await message.answer("Вибирете что нужно изменить👌: ", reply_markup=settings_button)


@router.message(F.text.startswith("Изменить"))
async def router_message(message: Message):
    change = message.text.split()[1]
    match change:
        case "Пол":
            await change_sex(message)
        case "Возраст":
            await message.answer("Выберете возраст👴: ", reply_markup=change_age_markup(0, 36))
        case "VIP":
            await prepare_invoice(message)
        case _:
            await message.answer("Unknown")


@router.callback_query(F.data.startswith("sex_"))
async def router_message(query: CallbackQuery):
    await change_query_sex(query)


@router.callback_query(F.data.startswith("pag_"))
async def router_message(query: CallbackQuery):
    markup = change_age_markup(int(query.data.split("_")[1]), int(query.data.split("_")[2]))
    await query.answer("Выберете возраст!")
    await query.message.edit_text(text="Выберете возраст👷‍♂️!", reply_markup=markup)


@router.callback_query(F.data.startswith("age_"))
async def router_message(query: CallbackQuery):
    age = int(query.data.split("_")[1])
    await run_sql(UpdateUser(query.from_user.id, age=age))
    await query.answer(f"Возраст изменен на {age}!", show_alert=True)
    await query.message.answer("Виберете что нужно изменить👌: ", reply_markup=settings_button)


@router.message(F.text == 'Мой профиль!')
async def router_message(message: Message, user: Users):
    await message.answer(user.__str__())
