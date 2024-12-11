from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from api.keyboards.buttons import chat_settings_buttons
from api.keyboards.keyboard import EnumKeyboardMarkup
from api.settings.sex.util import translate
from api.settings.user_age_settings import change_age_markup
from db.sql.enum.enums import ChatSettingsSex
from db.sql.model import Users
from db.sql.service import run_sql, UpdateChatSettings
from middlewares.middleware import AuthMiddleware, AuthCallbackMiddleware

router = Router()
router.message.middleware(AuthMiddleware())
router.callback_query.middleware(AuthCallbackMiddleware())


@router.message(F.text == "Поменять настройки пред почитания!")
async def perpose(message: Message):
    await message.answer("Выберете что нужно поменять 😽", reply_markup=chat_settings_buttons)


@router.message(F.text == "Поменять подходящий пол")
async def chat_settings(message: Message):
    markup = EnumKeyboardMarkup(ChatSettingsSex, "chs_", name_func=lambda el: translate(el.value))
    await message.answer("Выбери подходящий тебе пол ♂️: ", reply_markup=markup.as_keyboard_markup())


@router.callback_query(F.data.startswith("cpag_"))
async def router_message(query: CallbackQuery, user: Users):
    from_age = query.data.split("_")[1]
    if from_age == 'min':
        markup = change_age_markup(int(query.data.split("_")[2]), int(query.data.split("_")[3]), prefix="cage_min_",
                                   pag_prefix="cpag_min_", max_limit=(int(user.chat_settings.max_age) - 1))
    elif from_age == 'max':
        markup = change_age_markup(int(query.data.split("_")[2]), int(query.data.split("_")[3]), prefix="cage_max_",
                                   pag_prefix="cpag_max_", min_limit=(int(user.chat_settings.min_age) - 1))
    else:
        markup = None
    await query.answer("Выберете возраст🧑!")
    await query.message.edit_text(text="Выберете возраст 👌", reply_markup=markup)


@router.callback_query(F.data.startswith("cage_"))
async def router_message(query: CallbackQuery, user: Users):
    from_age = query.data.split("_")[1]
    age = int(query.data.split("_")[2])
    if from_age == 'min':
        await run_sql(UpdateChatSettings(user.tg_id, age_min=age))
    elif from_age == 'max':
        await run_sql(UpdateChatSettings(user.tg_id, age_max=age))
    await query.answer("Возраст для пред почитания успешно изменен✌️!!!")
    await query.message.delete()


@router.callback_query(F.data.startswith("chs_"))
async def router_message(query: CallbackQuery):
    data = query.data.split("_")[1]
    chat_settings_sex = ChatSettingsSex(int(data))
    await run_sql(UpdateChatSettings(query.from_user.id, sex=chat_settings_sex))
    await query.answer("Успешно обновлено👏!")
    await query.message.delete()


@router.message(F.text == "Максимальный возраст")
async def chat_settings(message: Message, user: Users):
    markup = change_age_markup(0, 36, prefix="cage_max_",
                               pag_prefix="cpag_max_", min_limit=(int(user.chat_settings.min_age) - 1))
    await message.answer(text="Выберете возраст🧑!", reply_markup=markup)


@router.message(F.text == "Минимальный возраст")
async def chat_settings(message: Message, user: Users):
    markup = change_age_markup(0, 36, prefix="cage_min_",
                               pag_prefix="cpag_min_", max_limit=(int(user.chat_settings.max_age) - 1))
    await message.answer(text="Выберете возраст🧑!", reply_markup=markup)


@router.message(F.text == "Назад к прошлым настройкам.")
async def chat_settings(message: Message, user: Users):
    settings_button = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Изменить Пол"), KeyboardButton(text="Изменить Возраст"),
         KeyboardButton(text="Изменить VIP")],
        [KeyboardButton(text="Поменять настройки пред почитания!")],
        [KeyboardButton(text="Мой профиль!")],
        [KeyboardButton(text="Назад к чату")]
    ], resize_keyboard=True)
    await message.answer("Выберите что нужно изменить 👌: ", reply_markup=settings_button)
