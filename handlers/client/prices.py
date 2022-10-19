from aiogram import Router, F, types
from aiogram.dispatcher.fsm.context import FSMContext
from handlers.client.main_menu import commands_start
from utils.language_distributor import distributor

router = Router()
router.message.filter()

flags = {"throttling_key": "True"}


@router.message(F.text.in_({'⬅️ Назад', '⬅️ Back', '⬅️ Orqaga'}), flags=flags)
async def back(message: types.Message, state: FSMContext):
    await commands_start(message, state)


@router.message((F.text.in_({"🎁 Готовое решение", "🎁 Tayyor yechim", "🎁 Ready solution"})), flags=flags)
async def turnkey_solution(message: types.Message):
    text_1 = await distributor(message.from_user.id, 'turnkey_solution_1')
    text_2 = await distributor(message.from_user.id, 'turnkey_solution_2')
    text_3 = await distributor(message.from_user.id, 'turnkey_solution_3')
    await message.answer(text_1)
    await message.answer(text_2)
    await message.answer(text_3)


@router.message((F.text.in_({"🗝 Индивидуальная разработка", "🗝 Individual development", "🗝 Shaxsiy rivojlanish"})),
                flags=flags)
async def individual_price(message: types.Message):
    text_1 = await distributor(message.from_user.id, 'individual_price_1')
    text_2 = await distributor(message.from_user.id, 'individual_price_2')
    await message.answer(text_1)
    await message.answer(text_2)
