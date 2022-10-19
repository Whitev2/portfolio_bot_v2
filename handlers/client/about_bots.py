import asyncio
from aiogram import Router, F, types
from aiogram.dispatcher.fsm.context import FSMContext
from handlers.client.main_menu import commands_start
from states.about_bots_state import About_menu
from utils.language_distributor import distributor

router = Router()
router.message.filter(state=About_menu)

flags = {"throttling_key": "True"}


@router.message(F.text.in_({'⬅️ Назад', '⬅️ Back', '⬅️ Orqaga'}))
async def back(message: types.Message, state: FSMContext):
    await commands_start(message, state)


@router.message((F.text.in_({"❇️  Плюсы", "❇️ Pros"})))
async def pross(message: types.Message):
    text_1 = await distributor(message.from_user.id, 'pross_1')
    text_2 = await distributor(message.from_user.id, 'pross_2')
    await message.answer(text_1)
    await asyncio.sleep(3)
    await message.answer(text_2)


@router.message((F.text.in_({'❕ Что умеют чат-боты', "❕ What Chatbots Can Do", "❕ Chatbotlar nima qila oladi"})))
async def what_can(message: types.Message):
    text = await distributor(message.from_user.id, 'what_can')
    await message.answer(text)


@router.message(
    (F.text.in_({'⚜️ Преимущества чат-ботов', "⚜️ Benefits of Chatbots", "⚜️ Chatbotlarning afzalliklari"})))
async def advantages(message: types.Message):
    text = await distributor(message.from_user.id, 'advantages')
    await message.answer(text)


@router.message((F.text.in_({'🕵🏼‍♀️ Сферы применения', "🕵🏼‍♀️ Who needs", "🕵🏼‍♀️ Kimga kerak"})))
async def spheres(message: types.Message):
    text = await distributor(message.from_user.id, 'spheres')
    await message.answer(text)
