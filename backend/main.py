from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from fastapi import FastAPI, Body, Depends, HTTPException
from src.model import UserSchema, UserLoginSchema, UserBaseSchema, UserCreateSchema
from src.auth.jwt_handler import signJWT
from src.database import User, resetDB
from bson import ObjectId

from src.auth.jwt_bearer import jwtBearer

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["test"])
def test():
    return User.find_one({'username' : "test"})

@app.get("/reset", tags=["test"])
async def reset():
     await resetDB()
     return {"message": "Database reset complete!"}

@app.post("/api/login", tags=["Login"])
def user_login(user: UserLoginSchema = Body(default=None)):
    if user != None:
        user_data = User.find_one(user.model_dump())
        if user_data:
            return signJWT(user_data['name'], user_data['surname'], user_data['username'], user_data['is_admin'])
        else:
            return {
                "error": "Invalid login!"
            }
        
@app.get("/api/users", dependencies=[Depends(jwtBearer())], tags=["User administration"])
def users_list():
    users = []
    cursor = User.find({})
    for user in cursor:
        user_id = str(user.pop("_id"))
        users.append(UserSchema(id=user_id, **user))
    return {"users": users}

@app.post("/api/users", dependencies=[Depends(jwtBearer())], tags=["User administration"])
def create_user(user: UserCreateSchema = Body(default=None)):
    User.insert_one(user.model_dump())

@app.put("/api/users/{user_id}", dependencies=[Depends(jwtBearer())], response_model=UserSchema, tags=["User administration"])
async def update_user(user_id: str, user_data: UserBaseSchema):
    existing_user = User.find_one({"_id": ObjectId(user_id)})
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = User.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user_data.model_dump()},
    )
    updated_user = User.find_one({"_id": ObjectId(user_id)})
    return UserSchema(id=str(updated_user['_id']), **user_data.dict())

@app.delete("/api/users/{user_id}", dependencies=[Depends(jwtBearer())], tags=["User administration"])
async def delete_user(user_id: str):
    deleted_user = User.delete_one({"_id": ObjectId(user_id)})
    if deleted_user.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}