from database.db import mongo_easy_find_one


async def distributor(telegram_id: int, tag: str) -> [str, bool]:
    """This function returns text depending on the selected language"""

    user_info = await mongo_easy_find_one('database', 'user_info', {'_id': int(telegram_id)})
    language = user_info.get('language')
    text = await mongo_easy_find_one('database', 'texts', {'$and': [{'tag': str(tag)}, {'language': language}]})
    return text.get('text')