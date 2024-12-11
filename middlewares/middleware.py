from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from api.keyboards.buttons import location_button
from api.settings.user_age_settings import change_age_markup
from db.sql.model import Users
from db.sql.service import ReadUser, run_sql, CreateUser


class AuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        print("username = ", event.from_user.username)
        result: Users = await run_sql(ReadUser(event.from_user.id))
        if result is None:
            last_name = event.from_user.last_name or f"Не указано"
            print(f"LASTNAME: {last_name}")
            await run_sql(
                CreateUser(event.from_user.id,
                           event.from_user.username or f"user_{event.from_user.id}",
                           event.from_user.first_name or f"Не указано",
                           last_name))
            await event.answer("Пожалуйста укажите место проживания!👌", reply_markup=location_button)
            return
        if result.location is None:
            await event.answer("Пожалуйста укажите место проживания!👌", reply_markup=location_button)
            return
        if result.age == -1:
            await event.answer("Укажите свой возраст!🥱",
                               reply_markup=change_age_markup(0, 36, prefix="sage_", pag_prefix="spag_"))
            return
        data['user'] = result
        return await handler(event, data)


class AuthCallbackMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        print("username = ", event.from_user.username)
        result = await run_sql(ReadUser(event.from_user.id))
        if result is None:
            result = await run_sql(CreateUser(event.from_user.id))
        data['user'] = result
        return await handler(event, data)
