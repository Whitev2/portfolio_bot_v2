from aiogram import types
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from data import all_data

data = all_data()


def main_admin_menu():
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Добавить текст"))
    nmarkup.row(types.KeyboardButton(text="Добавить клавиатуру"))
    nmarkup.row(types.KeyboardButton(text="Статистика"))
    nmarkup.row(types.KeyboardButton(text="Рассылка"))
    nmarkup.row(types.KeyboardButton(text="Возврат в меню"))
    return nmarkup.as_markup(resize_keyboard=True)