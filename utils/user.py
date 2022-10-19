from aiogram.types import Message

from database.db import mongo_easy_find_one


class User:
    def __init__(self, message: Message):
        self.user_id = int(message.from_user.id)

    async def get_language(self):
        user_info = await mongo_easy_find_one('database', 'user_info', {'_id': self.user_id})
        return user_info.get('language')