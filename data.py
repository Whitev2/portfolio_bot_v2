import os

import motor.motor_asyncio
import psycopg2
from aiogram import Bot
from redis import from_url


class all_data():
    def __init__(self):
        self.redis_url = os.getenv('REDIS_URL')
        self.bot_token = os.getenv('BOT_TOKEN')
        self.mg_user = os.getenv('MONGO_INITDB_ROOT_USERNAME')
        self.mg_pswd = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
        self.mg_host = os.getenv('MONGO_HOST')
        self.mg_port = os.getenv('MONGO_PORT')
        self.super_admins = (2036190335, )
        self.THROTTLE_TIME = 0.8

# фывфывфдв
    def get_bot(self):
        return Bot(self.bot_token, parse_mode="HTML")


    def get_mongo(self):
        return motor.motor_asyncio.AsyncIOMotorClient(username=self.mg_user, password=self.mg_pswd,
                                                      host=self.mg_host, port=int(self.mg_port))

    def get_red(self):
        return from_url(self.redis_url, decode_responses=True)

    def get_data_red(self):
        return from_url(f'{self.redis_url}/1', decode_responses=True)



#Settings:

Check_tickets = True
