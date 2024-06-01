import pymongo
from pymongo import mongo_client
from decouple import config
from src.model import UserCreateSchema, UserTypeBaseSchema

client = mongo_client.MongoClient(config("mongo_url"))

print('Connected to MongoDB...')

db = client[config("mongo_db")]

User = db.users
UserType = db.users_types
Incident = db.incidents

async def resetDB():
    for collection_name in db.list_collection_names():
        db[collection_name].drop()
        print(collection_name)
    await initialData()
    await createInitialAdminUser()
    print("Database reset complete")

async def createInitialAdminUser():
    user_data = UserCreateSchema(
        name="Default",
        surname="Admin",
        username="admin",
        password="admin",
        type=None,
        is_admin=True
    )
    User.insert_one(user_data.model_dump())
    print("Default user created")

async def initialData():
    data = UserTypeBaseSchema(name='JVP')
    UserType.insert_one(data.model_dump())
    data = UserTypeBaseSchema(name='DVD')
    UserType.insert_one(data.model_dump())
    print("Default user types created")