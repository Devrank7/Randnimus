from aiogram import Router, F
from aiogram.filters import CommandStart, Command
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


@router.message(Command("info"))
async def info_router(message: Message):
    text = """Главная цель бота, \n
     это общение 👨‍💻 с незнакомыми людьми 👤️ через нашего бота, переписка разними сообщениями с \n
      каким то анонимными людьми💼, которых вы можете настроить🔧 по Полу, возрасту и т.д \n
      Вы также можете настроить ⚖️ свой профиль для нахождения более привлекательных партнеров. \n
      Для VIP пользователей👑 мы предоставляем больше интересных возможностей, \n
      как например👓 видеть имя, возраст, пол и даже шде проживает человек с которым \n
      мы анонимно общаетесь. Для получения VIP💎 нужно заплатить 10 долларов💳💰 на неделю, \n
      но оно того стоит.
      """
    await message.answer(f"О чем проект? \n {text}")
