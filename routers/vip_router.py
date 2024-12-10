from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.types import PreCheckoutQuery, Message

from api.settings.user_vip_settings import give_vip_on
from middlewares.middleware import AuthMiddleware

router = Router()
router.message.middleware(AuthMiddleware())


@router.pre_checkout_query(lambda query: True)
def pre_checkout_query(query: PreCheckoutQuery):
    return query.answer(ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def payment(message: Message):
    await give_vip_on(message, 7)
