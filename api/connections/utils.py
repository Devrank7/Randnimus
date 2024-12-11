from aiogram.types import Message

from api.location.location import get_city_from_coordinates, get_city_by_coordinates
from db.sql.model import Users
from db.sql.service import run_sql, ReadConnection


def prepare_id(message: Message, first_user_id, second_user_id):
    data = {
        "sender": message.from_user.id,
        "consumer": second_user_id if message.from_user.id == first_user_id else first_user_id
    }
    return data


async def check_and_notify_connect(message: Message) -> bool:
    connect, first_user_id, second_user_id = await run_sql(ReadConnection(message.from_user.id))
    if first_user_id != -1 and second_user_id != -1:
        await message.answer("Вы уже связанны с другим человеком! 🤠")
    return first_user_id != -1 and second_user_id != -1


def get_info(user: Users, is_vip) -> str:
    if is_vip:
        city = get_city_by_coordinates(user.location.latitude, user.location.longitude)
        first_name = user.first_name
        last_name = user.last_name
        username = user.username
        text = f"Данные: Телеграм имя @{username}, \n Имя: {first_name}, \n Фамилия: {last_name}, \n " \
               f"Возраст {user.age}, \n Пол: {user.sex} \n Место проживания: {city}"
        return text
    return "Если хотите узнать все данные об пользователе покупайте VIP 💎"
