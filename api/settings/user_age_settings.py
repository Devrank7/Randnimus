from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

MAX_AGE = 140
MIN_AGE = 1


def change_age_markup(min_age: int, max_age: int, min_limit: int = MIN_AGE,
                      max_limit: int = MAX_AGE, prefix: str = "age_",
                      pag_prefix: str = "pag_") -> InlineKeyboardMarkup:
    min_v = min(max(min_limit, min_age), max_limit)
    max_v = min(max(min_limit, max_age), max_limit)
    builder = InlineKeyboardBuilder()
    for i in range(min_v, max_v):
        builder.button(text=str(i), callback_data=f"{prefix}{str(i)}")
    builder.adjust(6)
    bottom_buttons = []
    if max_v < max_limit:
        bottom_buttons.append(
            InlineKeyboardButton(text=">>", callback_data=f'{pag_prefix}{int(min_v) + 35}_{int(max_v) + 36}'))
    if min_v > min_limit:
        bottom_buttons.insert(0,
                              InlineKeyboardButton(text="<<",
                                                   callback_data=f'{pag_prefix}{int(min_v) - 36}_{int(min_v) - 1}'))
    if len(bottom_buttons) == 1:
        builder.row(*bottom_buttons)
    elif len(bottom_buttons) == 2:
        builder.row(*bottom_buttons)
    return builder.as_markup()
