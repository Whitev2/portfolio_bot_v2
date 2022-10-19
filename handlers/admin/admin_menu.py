from aiogram import Router, F, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database.db import mongo_easy_insert
from handlers.client.main_menu import select_language, commands_start
from states.admin_state import Admin_menu

router = Router()
router.message.filter(state=Admin_menu)

flags = {"throttling_key": "True"}


@router.message(F.text.in_({'Возврат в меню'}), flags=flags)
async def back(message: types.Message, state: FSMContext):
    await commands_start(message, state)


@router.message((F.text == "Добавить текст"), flags=flags)
async def new_text(message: Message, state: FSMContext):
    await state.set_state(Admin_menu.confirm_text)
    text = 'Напишите текст в формате tag|language|text'
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Отменить"))
    await message.answer(text, reply_markup=nmarkup.as_markup(resize_keyboard=True))


@router.message(state=Admin_menu.confirm_text, flags=flags)
async def confirm_text(message: Message, state: FSMContext):
    text = message.html_text.split('|')
    await message.answer('Ваш текст:\n\n'
                         f'Тег: {text[0]}\n'
                         f'Язык: {text[1]}\n'
                         f'Текст:\n\n{text[-1]}')
    await mongo_easy_insert('database', 'texts', {'tag': text[0], 'language': text[1], 'text': text[-1]})
    await state.clear()
    await select_language(message, state)


@router.message((F.text == "Добавить клавиатуру"), flags=flags)
async def new_keyboard(message: Message, state: FSMContext):
    await state.set_state(Admin_menu.confirm_keyboard)
    text = 'Напишите текст в формате tag|language|button_1, button_2..'
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Отменить"))
    await message.answer(text, reply_markup=nmarkup.as_markup(resize_keyboard=True))


@router.message(state=Admin_menu.confirm_keyboard, flags=flags)
async def confirm_keyboard(message: Message, state: FSMContext):
    keyboard_info = message.html_text.split('|')
    buttons = keyboard_info[-1].split(',')
    await message.answer('Клавиатура добавлена')
    await mongo_easy_insert('database', 'keyboard',
                            {'tag': keyboard_info[0], 'language': keyboard_info[1], 'buttons': buttons})
    await state.clear()
    await select_language(message, state)


@router.message((F.text == "Статистика"), flags=flags)
async def statistics(message: Message, state: FSMContext):
    pass


@router.message((F.text == "Рассылка"), flags=flags)
async def spam(message: Message, state: FSMContext):
    pass
