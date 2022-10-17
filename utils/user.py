from aiogram.types import Message

from database.db import mongo_easy_find_one


class User:
    def __init__(self, message: Message):
        self.user_id = int(message.from_user.id)

    async def get_language(self):
        print(111111)
        print(self.user_id)
        user_info = await mongo_easy_find_one('database', 'user_info', {'_id': self.user_id})
        print(user_info)
        return user_info.get('language')