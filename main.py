import asyncio
from datetime import datetime
from aiogram import Dispatcher
from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from data import all_data
from handlers.admin import admin_menu
from handlers.client import main_menu, about_bots, prices, order_bot

data = all_data()
bot = data.get_bot()
storage = RedisStorage.from_url(data.redis_url)
dp = Dispatcher(storage)


async def periodic():
    print('periodic function has been started')
    while True:
        c_time = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime('%Y.%m.%d')

        await asyncio.sleep(1)


async def main():
    bot_info = await bot.get_me()
    print(f"Hello, i'm {bot_info.first_name} | {bot_info.username}")


    dp.include_router(main_menu.router)
    dp.include_router(admin_menu.router)
    dp.include_router(about_bots.router)
    dp.include_router(prices.router)
    dp.include_router(order_bot.router)

    #periodic function
    asyncio.create_task(periodic())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
