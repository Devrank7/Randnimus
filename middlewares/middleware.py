from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from db.sql.service import ReadUser, run_sql, CreateUser


class AuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        print("username = ", event.from_user.username)
        result = await run_sql(ReadUser(event.from_user.id))
        if result is None:
            result = await run_sql(CreateUser(event.from_user.id))
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
