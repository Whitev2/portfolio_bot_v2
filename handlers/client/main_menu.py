from aiogram import Router, F, types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database.db import mongo_easy_insert, mongo_easy_upsert
from keyboards.admin_kb.admin_reply_kb import main_admin_menu
from states.about_bots_state import About_menu
from states.admin_state import Admin_menu
from states.order_bot_state import Order_bots
from utils.keyboard_returner import keyboard
from utils.language_distributor import distributor

router = Router()
router.message.filter()
flags = {"throttling_key": "True"}


@router.message(commands=['start', 'help', 'restart'], state='*', flags=flags)
async def commands_start(message: Message, state: FSMContext):
    await state.clear()
    if await mongo_easy_insert('database', 'user_info', {'_id': message.from_user.id, 'datetime_come': message.date,
                                                         'username': message.from_user.username}) is not False:
        nmarkup = ReplyKeyboardBuilder()
        nmarkup.row(types.KeyboardButton(text="🇷🇺 Русский 🇷🇺"))
        nmarkup.row(types.KeyboardButton(text="🇺🇸 English 🇺🇸"))
        nmarkup.row(types.KeyboardButton(text="🇺🇿 O'zbek 🇺🇿"))
        await message.answer('Hello! Please select a language!', reply_markup=nmarkup.as_markup(resize_keyboard=True))
    else:
        await select_language(message, state)


@router.message(((F.text == "🇷🇺 Русский 🇷🇺") | (F.text == "🇺🇸 English 🇺🇸") | (F.text == "🇺🇿 O'zbek 🇺🇿")), flags=flags)
async def select_language(message: Message, state: FSMContext):
    if 'English' in message.text:
        await mongo_easy_upsert('database', 'user_info', {'_id': int(message.from_user.id)}, {'language': 'en'})
    elif 'Русский' in message.text:
        await mongo_easy_upsert('database', 'user_info', {'_id': int(message.from_user.id)}, {'language': 'ru'})
    elif "O'zbek" in message.text:
        await mongo_easy_upsert('database', 'user_info', {'_id': int(message.from_user.id)}, {'language': 'uz'})

    text = await distributor(message.from_user.id, 'hello_world')
    await message.answer(text, reply_markup=await keyboard(message, 'hello_world', adjust=2))


@router.message((F.text.in_({"♻️ Change language", "♻️ Tilni o'zgartirish", "♻️  Сменить язык"})), flags=flags)
async def other_bot(message: types.Message, state: FSMContext):
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="🇷🇺 Русский 🇷🇺"))
    nmarkup.row(types.KeyboardButton(text="🇺🇸 English 🇺🇸"))
    nmarkup.row(types.KeyboardButton(text="🇺🇿 O'zbek 🇺🇿"))
    await message.answer('Please select a language!', reply_markup=nmarkup.as_markup(resize_keyboard=True))

@router.message((F.text.in_({"❔️О чат-ботах", "❔️ About chatbots", "❔️ Chatbotlar haqida"})), flags=flags)
async def other_bot(message: types.Message, state: FSMContext):
    await state.set_state(About_menu.main)
    text = await distributor(message.from_user.id, 'other_bot')
    await message.answer(text, reply_markup=await keyboard(message, 'other_bot', adjust=2))


@router.message((F.text.in_({"📝Заказать бота", "📝 Order a bot", "📝 Botga buyurtma bering"})), flags=flags)
async def new_order(message: types.Message, state: FSMContext):
    await state.set_state(Order_bots.user_name)
    text = await distributor(message.from_user.id, 'new_order')
    await message.answer(text, reply_markup=await keyboard(message, 'back', adjust=2))


@router.message((F.text.in_({"💸 Цены", "💸 Prices", "💸 Narxlar"})), flags=flags)
async def prices(message: types.Message, state: FSMContext):
    await state.set_state(About_menu.main)
    text = await distributor(message.from_user.id, 'other_bot')
    await message.answer(text, reply_markup=await keyboard(message, 'prices', adjust=2))


@router.message((F.text.in_({"🥽 Bot examples", "🥽 Примеры ботов", "🥽 Bot misollar"})), flags=flags)
async def bot_example(message: types.Message):
    text = await distributor(message.from_user.id, 'bot_example')
    await message.answer(text, disable_web_page_preview=True)


@router.message((F.text.in_({"📢 Feedback", "📢 Обратная связь", "📢 Qayta aloqa"})), flags=flags)
async def feedback(message: types.Message):
    text = await distributor(message.from_user.id, 'feedback')
    await message.answer(text, disable_web_page_preview=True)

@router.message((F.text == "♻️ Админ"), flags=flags)
async def admin_menu(message: Message, state: FSMContext):
    await state.set_state(Admin_menu.main)
    text = 'Добро пожаловать в режим администрации'
    await message.answer(text, reply_markup=main_admin_menu())
