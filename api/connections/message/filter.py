from typing import Any, Union, Dict

from aiogram.filters import Filter
from aiogram.types import Message

from api.connections.message.connect_exchange import exchanges


class ContentFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.content_type in exchanges.keys()
