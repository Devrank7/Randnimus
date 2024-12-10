from aiogram import Router, F
from aiogram.types import CallbackQuery

from api.settings.user_age_settings import change_age_markup
from api.settings.user_sex_settings import change_sex, change_or_register
from db.sql.service import UpdateUser, run_sql

router = Router()


@router.callback_query(F.data.startswith("spag_"))
async def router_message(query: CallbackQuery):
    markup = change_age_markup(int(query.data.split("_")[1]), int(query.data.split("_")[2]), pag_prefix="spag_",
                               prefix="sage_")
    await query.answer("Выберете возраст!")
    await query.message.edit_text(text="Выберете возраст!", reply_markup=markup)


@router.callback_query(F.data.startswith("sage_"))
async def router_message(query: CallbackQuery):
    age = int(query.data.split("_")[1])
    await run_sql(UpdateUser(query.from_user.id, age=age))
    await query.answer(f"Возраст изменен на {age}!", show_alert=True)
    await query.message.delete()
    await change_sex(query.message, "Теперь выберете ваш пол", "ssex_")


@router.callback_query(F.data.startswith("ssex_"))
async def router_message(query: CallbackQuery):
    await change_or_register(query)
