from aiogram import types
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from data import all_data
from database.db import mongo_easy_find_one
from utils.user import User

data = all_data()


async def main_kb(message: Message):
    user = User(message)
    language = user.get_language()

    user_id = int(message.from_user.id)
    keyboard = await mongo_easy_find_one('database', 'keyboards', {'$and': [{'_id': user_id}, {'language': language}]})
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="📝 Заказать бота"))
    nmarkup.row(types.KeyboardButton(text="❔️ О чат-ботах"))
    nmarkup.row(types.KeyboardButton(text="🥽 Примеры ботов"))
    nmarkup.row(types.KeyboardButton(text="💸 Цены"))
    nmarkup.row(types.KeyboardButton(text="📢 Обратная связь"))
    nmarkup.adjust(1, 2, 1, 1)
    if user_id in data.super_admins:
        nmarkup.row(types.KeyboardButton(text="♻️ Админ"))
    return nmarkup.as_markup(resize_keyboard=True)
