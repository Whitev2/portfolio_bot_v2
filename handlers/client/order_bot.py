import asyncio
from aiogram import Router, F, types
from aiogram.dispatcher.fsm.context import FSMContext

from data import all_data
from handlers.client.main_menu import commands_start
from states.order_bot_state import Order_bots
from utils.language_distributor import distributor

router = Router()
router.message.filter(state=Order_bots)
flags = {"throttling_key": "True"}

data = all_data()
bot = data.get_bot()

@router.message(F.text.in_({'⬅️ Назад', '⬅️ Back', '⬅️ Orqaga'}), flags=flags)
async def back(message: types.Message, state: FSMContext):
    await commands_start(message, state)


@router.message(state=Order_bots.user_name, flags=flags)
async def order_user_name(message: types.Message, state: FSMContext):
    await state.update_data(username=message.html_text)
    await state.set_state(Order_bots.buissnes)
    text = await distributor(message.from_user.id, 'order_user_name')
    await message.answer(text)


@router.message(Order_bots.buissnes, flags=flags)
async def order_buisnes(message: types.Message, state: FSMContext):
    await state.update_data(buisnes=message.html_text)
    await state.set_state(Order_bots.order_confirm)
    text = await distributor(message.from_user.id, 'order_buisnes')
    await message.answer(text)


@router.message(Order_bots.order_confirm, flags=flags)
async def order_confirm(message: types.Message, state: FSMContext):
    data = await state.get_data()
    order = dict()
    order['name'] = data['username']
    order['buisnes'] = data['buisnes']
    order['contact'] = message.html_text
    order['username_tg'] = message.from_user.username

    await asyncio.create_task(order_send_to_admins(order))
    text = await distributor(message.from_user.id, 'order_confirm')
    await message.answer(text)
    await asyncio.sleep(2)
    await commands_start(message, state)


async def order_send_to_admins(order):
    try:
        await bot.send_message(chat_id=all_data().super_admins[0], text=f'У вас новая заявка:\n\nИмя: {order["name"]}\n'
                                                                    f'Контакт телеграм: @{order["username_tg"]}\n\n'
                                                                    f'Контакт для связи: {order["contact"]}\n'
                                                                    f'Бизнес: {order["buisnes"]}\n')
    except Exception:
        pass