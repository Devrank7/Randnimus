from abc import ABC, abstractmethod
from enum import Enum

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class KeyboardsMarkup(ABC):
    @abstractmethod
    def as_keyboard_markup(self) -> InlineKeyboardMarkup:
        raise NotImplementedError


class EnumKeyboardMarkup(KeyboardsMarkup):

    def __init__(self, type_enum, callback_prefix: str, delimiter: int = 3):
        self.type_enum = type_enum
        self.delimiter = delimiter
        self.callback_prefix = callback_prefix

    def as_keyboard_markup(self) -> InlineKeyboardMarkup:
        keyboard_builder = InlineKeyboardBuilder()
        for element in self.type_enum:
            keyboard_builder.button(
                text=element.name,
                callback_data=f"{self.callback_prefix}{str(element.value)}"
            )
        keyboard_builder.adjust(self.delimiter)
        return keyboard_builder.as_markup()
