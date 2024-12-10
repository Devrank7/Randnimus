from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

disconnect_buttons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отключится")]
])
chat_settings_buttons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Поменять подходящий пол")],
    [KeyboardButton(text="Максимальный возраст"), KeyboardButton(text="Минимальный возраст")],
    [KeyboardButton(text="Назад к прошлым настройкам.")]
])
settings_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Изменить Пол"), KeyboardButton(text="Изменить Возраст"),
     KeyboardButton(text="Изменить VIP")],
    [KeyboardButton(text="Поменять настройки пред почитания!")],
    [KeyboardButton(text="Мой профиль!")],
    [KeyboardButton(text="Назад к чату")]
], resize_keyboard=True)
button_chat = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Начать чат")],
    [KeyboardButton(text="Настройки")]
], resize_keyboard=True)
location_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Дать локации", request_location=True)]
])
