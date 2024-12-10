from aiogram.types import Message

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
        await message.answer("Вы уже связанны с другим человеком!")
    return first_user_id != -1 and second_user_id != -1
