from aiogram.dispatcher.fsm.state import StatesGroup, State


class Order_bots(StatesGroup):
    main = State()
    user_name = State()
    buissnes = State()
    order_confirm = State()
