import fastapi
import uvicorn
from fastapi import FastAPI, Body, Depends
from src.model import UserSchema, UserLoginSchema
from src.auth.jwt_handler import signJWT
from src.database import User, resetDB, createInitialUser

from src.auth.jwt_bearer import jwtBearer

app = FastAPI()

@app.get("/", tags=["test"])
def test():
    return User.find_one({'username' : "test"})

@app.get("/reset", tags=["test"])
async def reset():
     await resetDB()
     await createInitialUser()
     return {"message": "Database reset complete!"}

# User Login
@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(default=None)):
    if user != None:
        user_data = User.find_one(user.model_dump())
        if user_data:
            return signJWT(user_data['username'])
        else:
            return {
                "error": "Invalid login!"
            }
        
# User Login
@app.post("/user/create", dependencies=[Depends(jwtBearer())], tags=["user"])
def user_create(user: UserSchema = Body(default=None)):
    User.insert_one(user.model_dump())