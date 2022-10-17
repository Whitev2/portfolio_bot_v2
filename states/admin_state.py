from aiogram.dispatcher.fsm.state import StatesGroup, State


class Admin_menu(StatesGroup):
    main = State()
    confirm_text = State()
    confirm_keyboard = State()
