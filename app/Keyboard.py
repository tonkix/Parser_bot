from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv
import os

import app.db.requests as rq

load_dotenv()
ADMIN_ROLE = os.getenv("ADMIN_ROLE")


async def main_kb(user_tg_id: int):
    kb_list = [
        [KeyboardButton(text="1"), KeyboardButton(text="2")]
    ]
    user = await rq.get_user_by_tg(user_tg_id)
    if user.role.__str__() == ADMIN_ROLE:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Меню:"
    )
    return keyboard
