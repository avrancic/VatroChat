import fastapi
import uvicorn
from fastapi import FastAPI
from model import UserSchema
from auth.jwt_handler import signJWT
# MongoDB Config
MONGO_URL = "mongodb+srv://avrancic:pVOdOWPUV8QkIE00@cluster0.r07sjwu.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB = "vatrochat_db"

app = FastAPI()

@app.get("/", tags=["test"])
def test():
    return {"test":"test"}