from aiogram import types
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from data import all_data
from database.db import mongo_easy_find_one
from utils.user import User

data = all_data()


async def keyboard(message: Message, tag, adjust: int):
    user = User(message)
    language = await user.get_language()
    user_id = int(message.from_user.id)
    keyboard = await mongo_easy_find_one('database', 'keyboard', {'$and': [{'tag': tag}, {'language': language}]})
    buttons_list = keyboard.get('buttons')
    nmarkup = ReplyKeyboardBuilder()
    for button in buttons_list:
        nmarkup.row(types.KeyboardButton(text=button))

    if tag == 'hello_world':
        if user_id in data.super_admins:
            nmarkup.row(types.KeyboardButton(text="♻️ Админ"))
    nmarkup.adjust(adjust)
    return nmarkup.as_markup(resize_keyboard=True)