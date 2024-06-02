from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from fastapi import FastAPI, Body, Depends, HTTPException
from src.model import UserSchema, UserLoginSchema, UserBaseSchema, UserUpdateSchema, UserCreateSchema, UserTypeSchema, IncidentSchema
from src.model import IncidentBaseSchema, IncidentSchema, IncidentWorkerSchema
from src.model import CommentBaseSchema, CommentSchema
from src.auth.jwt_handler import signJWT
from src.database import User, Incident, resetDB, UserType
from bson import ObjectId
from typing import List, Optional
from faker import Faker
import random
from datetime import timedelta
from fastapi.staticfiles import StaticFiles

from src.auth.jwt_bearer import jwtBearer

app = FastAPI()

faker = Faker()

origins = [
    "http://localhost:5173",
    "http://0.0.0.0:8000",
    "http://localhost:8000",
    "https://vatrochat-backend.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/init/resetdb", tags=["Initial"])
async def resetdb():
    await resetDB()
    return {"message": "Database reset complete!"}

@app.get("/init/create_fake_users", tags=["Initial"])
async def create_fake_users():
    user_type = UserType.find_one()

    if user_type is None:
        raise HTTPException(status_code=404, detail="No user type found")

    for _ in range(20):
        fake_user = UserCreateSchema(
            name=faker.first_name(),
            surname=faker.last_name(),
            username=faker.user_name(),
            password="12345",
            type=UserTypeSchema(id=str(user_type["_id"]), name=user_type["name"])
        )

        User.insert_one(fake_user.model_dump())
    return "Success"

@app.get("/init/create_fake_incidents", tags=["Initial"])
async def create_fake_incidents():
    for _ in range(20):
        cursor = User.find()
    
        users = list(cursor)

        # Convert each user to an IncidentWorkerSchema object
        incident_workers = []
        
        selected_users = random.sample(users, k=random.randint(1, min(5, len(users))))
        
        for user in selected_users:
            incident_worker = IncidentWorkerSchema(
                id=str(user['_id']),  # You might need to adjust these fields based on your User schema
                name=user['name'],  # You might need to adjust these fields based on your User schema
                surname=user['surname'],  # You might need to adjust these fields based on your User schema
                type=None  # Placeholder for user type; you'll need to adjust this based on your schema
            )
            incident_workers.append(incident_worker)
        
        open_from = faker.date_time_this_year()
        open_until = open_from + timedelta(days=faker.random_int(min=1, max=30))

        fake_incident = IncidentBaseSchema(
            title=faker.sentence(),
            location=faker.address(),
            open_from=open_from,
            open_until=open_until,
            workers=incident_workers
        )

        # Insert the fake incident into the database
        Incident.insert_one(fake_incident.model_dump())

    return "Success"

@app.post("/api/auth/login", tags=["Authentication"])
def user_login(login_data: UserLoginSchema = Body(default=None)):
    if login_data:
        user = User.find_one(login_data.model_dump())
        if user:
            return signJWT(
                user['name'], 
                user['surname'], 
                user['username'], 
                user['is_admin']
            )
        else:
            raise HTTPException(status_code=401, detail="Invalid login!")
    else:
        raise HTTPException(status_code=400, detail="No user data provided!")
                
@app.get("/api/users", response_model=List[UserSchema], tags=["User administration"]) #, dependencies=[Depends(jwtBearer())]
def users_list():
    users = User.find()
    return [{**user, "id": str(user["_id"])} for user in users]

@app.post("/api/users", response_model=UserSchema, tags=["User administration"])
def create_user(new_user_data: UserCreateSchema = Body(default=None)):
    insert_result = User.insert_one(new_user_data.model_dump())
    new_user = User.find_one({"_id": insert_result.inserted_id})
    new_user['id'] = str(new_user['_id'])
    return new_user

@app.put("/api/users/{user_id}", response_model=UserSchema, tags=["User administration"])
async def update_user(user_id: str, user_data: UserUpdateSchema):
    existing_user = User.find_one({"_id": ObjectId(user_id)})
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_data.password == None:
        del user_data.password
    
    User.update_one(
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
    user_types = UserType.find()
    return [{**user_type, "id": str(user_type["_id"])} for user_type in user_types]

@app.get("/api/incidents", response_model=List[IncidentSchema], tags=["Incidents"]) #, dependencies=[Depends(jwtBearer())]
async def incidents_list():
    incidents = Incident.find()
    return [{**incident, "id": str(incident["_id"])} for incident in incidents]

@app.post("/api/incidents", response_model=IncidentSchema, tags=["Incidents"])
async def create_incident(incident_data: IncidentBaseSchema = Body(default=None)):
    insert_result = Incident.insert_one(incident_data.model_dump())
    inserted_incident = Incident.find_one({"_id": insert_result.inserted_id})
    inserted_incident['id'] = str(inserted_incident['_id'])
    return inserted_incident

@app.put("/api/incidents/{id}", response_model=IncidentSchema, tags=["Incidents"])
async def update_incident(id: str, incident_data: IncidentBaseSchema):
    existing_incident = Incident.find_one({"_id": ObjectId(id)})
    if existing_incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    Incident.update_one(
        {"_id": ObjectId(id)},
        {"$set": incident_data.model_dump()},
    )
    updated_incident = Incident.find_one({"_id": ObjectId(id)})
    return IncidentSchema(id=str(updated_incident['_id']), **incident_data.dict())

@app.delete("/api/incidents/{id}", tags=["Incidents"])
async def delete_incident(id: str):
    deleted_incident = Incident.delete_one({"_id": ObjectId(id)})
    if deleted_incident.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Incident not found")
    return {"message": "Incident deleted successfully"}

@app.get("/api/incidents/workers", response_model=List[IncidentWorkerSchema], tags=["Incidents"])
async def incident_workers_list():
    workers = User.find()
    return [{**worker, "id": str(worker["_id"])} for worker in workers]