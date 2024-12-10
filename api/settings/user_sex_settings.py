from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

from api.keyboards.buttons import button_chat
from db.sql.enum.enums import Sex
from db.sql.service import run_sql, UpdateUser


async def change_sex(message: Message, text: str = "Выберете пол", prefix: str = "sex_"):
    sex_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Male", callback_data=f"{prefix}male"),
         InlineKeyboardButton(text="Female", callback_data=f"{prefix}sex_female")],
        [InlineKeyboardButton(text="Unknown", callback_data=f"{prefix}unknown")]
    ])
    await message.answer(text, reply_markup=sex_button)


async def change_query_sex(query: CallbackQuery):
    sex = query.data.split("_")[1]
    match sex:
        case "male":
            await run_sql(UpdateUser(query.from_user.id, Sex.MALE))
            await query.answer("Male")
            await query.message.answer("Change on male!")
        case "female":
            await run_sql(UpdateUser(query.from_user.id, Sex.FEMALE))
            await query.answer("Female")
            await query.message.answer("Change on female!")
        case "unknown":
            await run_sql(UpdateUser(query.from_user.id, Sex.UNKNOWN))
            await query.answer("Unknown")
            await query.message.answer("Change on unknown!")
        case _:
            await query.answer("Not found!", show_alert=True)


async def change_or_register(query: CallbackQuery):
    await change_query_sex(query)
    await query.message.delete()
    await query.message.answer("Вы успешно зарегистрировались", reply_markup=button_chat)
