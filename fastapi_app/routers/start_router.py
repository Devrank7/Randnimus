from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from api.location.location import get_city_by_coordinates
from db.sql.model import Users
from db.sql.service import run_sql, ReadUser
from main import bot

router = APIRouter()
templates = Jinja2Templates(directory="templates")


async def photo_url(user_id: int):
    user_photos = await bot.get_user_profile_photos(user_id)
    if user_photos.total_count > 0:
        photo = user_photos.photos[0][-1]
        file = await bot.get_file(photo.file_id)
        file_url = f'https://api.telegram.org/file/bot{bot.token}/{file.file_path}'
        return file_url
    return "https://www.shutterstock.com/image-vector/user-profile-icon-vector-avatar-600nw-2247726673.jpg"


@router.get("/{user_tg_id}")
async def get_user_data(request: Request, user_tg_id: int):
    user: Users = await run_sql(ReadUser(user_tg_id))
    url_photo = await photo_url(user_tg_id)
    location = user.location.latitude, user.location.longitude
    location = get_city_by_coordinates(latitude=location[0], longitude=location[1])
    return templates.TemplateResponse("result.html",
                                      {"request": request, "user": user, "url_photo": url_photo, "location": location})
