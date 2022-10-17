from data import all_data


async def mongo_easy_insert(database: str, collection: str, condition_dict: dict):
    """Use this function if you need to update or insert something and you not sure if it exists.\n\n
    Condition dict will be inserted too."""
    try:
        client = all_data().get_mongo()
        database = client[database]
        collection = database[collection]
        await collection.insert_one(condition_dict)
    except Exception as ex:
        return False

async def mongo_easy_upsert(database: str, collection: str, condition_dict: dict, main_dict: dict):
    """Use this function if you need to update or insert something and you not sure if it exists.\n\n
    Condition dict will be inserted too."""
    try:
        client = all_data().get_mongo()
        database = client[database]
        collection = database[collection]
        await collection.update_one(condition_dict, {"$set": main_dict})
    except Exception as ex:
        print(ex)


async def mongo_easy_find_one(database: str, collection: str, condition_dict: dict):
    """One select to rule them all."""
    try:
        client = all_data().get_mongo()
        database = client[database]
        collection = database[collection]
        return await collection.find_one(condition_dict)
    except Exception as ex:
        print(ex)