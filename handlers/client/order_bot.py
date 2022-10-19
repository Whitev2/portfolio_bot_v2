import asyncio
from aiogram import Router, F, types
from aiogram.dispatcher.fsm.context import FSMContext
from handlers.client.main_menu import commands_start
from states.order_bot_state import Order_bots
from utils.language_distributor import distributor

router = Router()
router.message.filter(state=Order_bots)
flags = {"throttling_key": "True"}


@router.message(F.text.in_({'⬅️ Назад', '⬅️ Back', '⬅️ Orqaga'}), flags=flags)
async def back(message: types.Message, state: FSMContext):
    await commands_start(message, state)


@router.message(state=Order_bots.user_name, flags=flags)
async def order_user_name(message: types.Message, state: FSMContext):
    await state.set_state(Order_bots.buissnes)
    text = await distributor(message.from_user.id, 'order_user_name')
    await message.answer(text)


@router.message(Order_bots.buissnes, flags=flags)
async def order_buisnes(message: types.Message, state: FSMContext):
    await state.set_state(Order_bots.order_confirm)
    text = await distributor(message.from_user.id, 'order_buisnes')
    await message.answer(text)


@router.message(Order_bots.order_confirm, flags=flags)
async def order_confirm(message: types.Message, state: FSMContext):
    text = await distributor(message.from_user.id, 'order_confirm')
    await message.answer(text)
    await asyncio.sleep(2)
    await commands_start(message, state)
