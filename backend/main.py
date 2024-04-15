from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from fastapi import FastAPI, Body, Depends, HTTPException
from src.model import UserSchema, UserLoginSchema, UserBaseSchema, UserCreateSchema, ShiftsSchema, UserTypeSchema, ShiftsBaseSchema
from src.auth.jwt_handler import signJWT
from src.database import User, resetDB, Shifts, UserType
from bson import ObjectId
from typing import List, Optional

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
        
@app.get("/api/users", response_model=List[UserSchema], tags=["User administration"]) #, dependencies=[Depends(jwtBearer())]
def users_list():
    items = User.find()
    return [{**i, "id": str(i["_id"])} for i in items]

@app.post("/api/users", tags=["User administration"])
def create_user(user: UserCreateSchema = Body(default=None)):
    User.insert_one(user.model_dump())

@app.put("/api/users/{user_id}", response_model=UserSchema, tags=["User administration"])
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

@app.delete("/api/users/{user_id}", tags=["User administration"])
async def delete_user(user_id: str):
    deleted_user = User.delete_one({"_id": ObjectId(user_id)})
    if deleted_user.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@app.get("/api/users/types", response_model=List[UserTypeSchema], tags=["User administration"])
async def users_types_list():
    items = UserType.find()
    return [{**i, "id": str(i["_id"])} for i in items]

@app.post("/api/shifts/", response_model=ShiftsSchema)
def create_shift(shift: ShiftsBaseSchema):
    shift_dict = shift.model_dump();
    inserted_shift = Shifts.insert_one(shift_dict)
    return {**shift_dict, "id": str(inserted_shift.inserted_id)}

@app.put("/api/shifts/{shift_id}", response_model=ShiftsSchema)
def update_shift(shift_id: str, shift: ShiftsBaseSchema):
    shift_dict = shift.model_dump(exclude_unset=True)
    result = Shifts.update_one({"_id": ObjectId(shift_id)}, {"$set": shift_dict})
    if result.modified_count == 1:
        return {**shift_dict, "id": shift_id}
    else:
        raise HTTPException(status_code=404, detail="Shift not found")

@app.delete("/api/shifts/{shift_id}")
def delete_shift(shift_id: str):
    result = Shifts.delete_one({"_id": ObjectId(shift_id)})
    if result.deleted_count == 1:
        return {"message": "Shift deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Shift not found")

@app.get("/api/shifts/", response_model=List[ShiftsSchema])
def list_shifts():
    shifts = Shifts.find()
    return [{**shift, "id": str(shift["_id"])} for shift in shifts]