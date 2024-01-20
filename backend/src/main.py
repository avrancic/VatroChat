import uvicorn
from fastapi import FastAPI

# MongoDB Config
MONGO_URL = "mongodb+srv://avrancic:pVOdOWPUV8QkIE00@cluster0.r07sjwu.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB = "vatrochat_db"

app = FastAPI()

@app.get("/", tags=["test"])
def test():
    return {"test":"test"}