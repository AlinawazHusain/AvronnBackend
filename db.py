from motor.motor_asyncio import AsyncIOMotorClient
import config
import datetime
import asyncio

client = AsyncIOMotorClient(config.CLIENT_URL)


async def InsertIntoDB(database_name, collection_name, data):
    try:
        db = client[database_name] 
        collection = db[collection_name]

        result = await collection.insert_one(data)

        return result.inserted_id
    except Exception as e:
        raise e

def AddValInStructure(input_data , dbstructure):
    data = dbstructure
    for i in input_data:
        data[i] = input_data[i]
    return data



async def user_exist(attribute ,Phone_number , database_name , collection_name):
    db = client[database_name]  
    collection = db[collection_name]

    user = await collection.find_one({str(attribute): Phone_number})
    if user:
        return True 
    else:
        return False 
    


async def get_data(attribute ,Phone_number , database_name , collection_name):
    db = client[database_name]  
    collection = db[collection_name]

    user = await collection.find_one({str(attribute): Phone_number})
    if user:
        return user
    else:
        return False



async def insertData(input_data , database_name , collection_name , dbstructure):
    data = AddValInStructure(input_data , dbstructure)
    inserted_id = await InsertIntoDB(database_name , collection_name, data)
    return inserted_id


