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
        nmarkup.row(types.KeyboardButton(text="๐ท๐บ ะ ัััะบะธะน ๐ท๐บ"))
        nmarkup.row(types.KeyboardButton(text="๐บ๐ธ English ๐บ๐ธ"))
        nmarkup.row(types.KeyboardButton(text="๐บ๐ฟ O'zbek ๐บ๐ฟ"))
        await message.answer('Hello! Please select a language!', reply_markup=nmarkup.as_markup(resize_keyboard=True))
    else:
        await select_language(message, state)


@router.message(((F.text == "๐ท๐บ ะ ัััะบะธะน ๐ท๐บ") | (F.text == "๐บ๐ธ English ๐บ๐ธ") | (F.text == "๐บ๐ฟ O'zbek ๐บ๐ฟ")), flags=flags)
async def select_language(message: Message, state: FSMContext):
    if 'English' in message.text:
        await mongo_easy_upsert('database', 'user_info', {'_id': int(message.from_user.id)}, {'language': 'en'})
    elif 'ะ ัััะบะธะน' in message.text:
        await mongo_easy_upsert('database', 'user_info', {'_id': int(message.from_user.id)}, {'language': 'ru'})
    elif "O'zbek" in message.text:
        await mongo_easy_upsert('database', 'user_info', {'_id': int(message.from_user.id)}, {'language': 'uz'})

    text = await distributor(message.from_user.id, 'hello_world')
    await message.answer(text, reply_markup=await keyboard(message, 'hello_world', adjust=2))


@router.message((F.text.in_({"โป๏ธ Change language", "โป๏ธ Tilni o'zgartirish", "โป๏ธ ะกะผะตะฝะธัั ัะทัะบ"})), flags=flags)
async def other_bot(message: types.Message, state: FSMContext):
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="๐ท๐บ ะ ัััะบะธะน ๐ท๐บ"))
    nmarkup.row(types.KeyboardButton(text="๐บ๐ธ English ๐บ๐ธ"))
    nmarkup.row(types.KeyboardButton(text="๐บ๐ฟ O'zbek ๐บ๐ฟ"))
    await message.answer('Please select a language!', reply_markup=nmarkup.as_markup(resize_keyboard=True))

@router.message((F.text.in_({"โ๏ธะ ัะฐั-ะฑะพัะฐั", "โ๏ธ About chatbots", "โ๏ธ Chatbotlar haqida"})), flags=flags)
async def other_bot(message: types.Message, state: FSMContext):
    await state.set_state(About_menu.main)
    text = await distributor(message.from_user.id, 'other_bot')
    await message.answer(text, reply_markup=await keyboard(message, 'other_bot', adjust=2))


@router.message((F.text.in_({"๐ะะฐะบะฐะทะฐัั ะฑะพัะฐ", "๐ Order a bot", "๐ Botga buyurtma bering"})), flags=flags)
async def new_order(message: types.Message, state: FSMContext):
    await state.set_state(Order_bots.user_name)
    text = await distributor(message.from_user.id, 'new_order')
    await message.answer(text, reply_markup=await keyboard(message, 'back', adjust=2))


@router.message((F.text.in_({"๐ธ ะฆะตะฝั", "๐ธ Prices", "๐ธ Narxlar"})), flags=flags)
async def prices(message: types.Message, state: FSMContext):
    await state.set_state(About_menu.main)
    text = await distributor(message.from_user.id, 'other_bot')
    await message.answer(text, reply_markup=await keyboard(message, 'prices', adjust=2))


@router.message((F.text.in_({"๐ฅฝ Bot examples", "๐ฅฝ ะัะธะผะตัั ะฑะพัะพะฒ", "๐ฅฝ Bot misollar"})), flags=flags)
async def bot_example(message: types.Message):
    text = await distributor(message.from_user.id, 'bot_example')
    await message.answer(text, disable_web_page_preview=True)


@router.message((F.text.in_({"๐ข Feedback", "๐ข ะะฑัะฐัะฝะฐั ัะฒัะทั", "๐ข Qayta aloqa"})), flags=flags)
async def feedback(message: types.Message):
    text = await distributor(message.from_user.id, 'feedback')
    await message.answer(text, disable_web_page_preview=True)

@router.message((F.text == "โป๏ธ ะะดะผะธะฝ"), flags=flags)
async def admin_menu(message: Message, state: FSMContext):
    await state.set_state(Admin_menu.main)
    text = 'ะะพะฑัะพ ะฟะพะถะฐะปะพะฒะฐัั ะฒ ัะตะถะธะผ ะฐะดะผะธะฝะธัััะฐัะธะธ'
    await message.answer(text, reply_markup=main_admin_menu())
