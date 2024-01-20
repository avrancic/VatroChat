import pymongo
from pymongo import mongo_client
from decouple import config
from src.model import UserSchema

client = mongo_client.MongoClient(config("mongo_url"))

print('Connected to MongoDB...')

db = client[config("mongo_db")]

User = db.users

async def resetDB():
    for collection_name in db.list_collection_names():
        db[collection_name].drop()
        print(collection_name)
    print("Database reset complete")

async def createInitialUser():
    user_data = UserSchema(
        ime="Default",
        prezime="Admin",
        username="admin",
        password="admin",
        is_admin=True
    )
    User.insert_one(user_data.model_dump())
    print("Default user created")