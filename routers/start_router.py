from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from api.keyboards.buttons import button_chat
from middlewares.middleware import AuthMiddleware

router = Router()
router.message.middleware(AuthMiddleware())


@router.message(CommandStart())
async def start_router(message: Message):
    await message.answer(f"Привет😘, {message.from_user.first_name}!, ознакомление с ботом /info 🎨",
                         reply_markup=button_chat)


@router.message(F.text == 'Назад к чату')
async def start_router(message: Message):
    await message.answer(f"Начните чат🙀, {message.from_user.first_name}!", reply_markup=button_chat)
