from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from fastapi import FastAPI, Body, Depends, HTTPException
from src.model import UserSchema, UserLoginSchema, UserBaseSchema, UserUpdateSchema, UserCreateSchema, UserTypeSchema, IncidentSchema
from src.model import IncidentBaseSchema, IncidentSchema, IncidentWorkerSchema
from src.model import CommentBaseSchema, CommentSchema, CommentCreateSchema, CommentDisplaySchema
from src.auth.jwt_handler import signJWT
from src.database import User, Incident, resetDB, UserType, Comment
from bson import ObjectId
from typing import List, Optional
from faker import Faker
import random
from datetime import timedelta
from fastapi.staticfiles import StaticFiles
from datetime import datetime

from src.auth.jwt_bearer import jwtBearer

app = FastAPI()

faker = Faker()

origins = [
    "http://localhost:10000",
    "http://0.0.0.0:10000",
    "http://localhost:10000",
    "https://vatrochat-frontend.onrender.com",
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

        incident_workers = []
        
        selected_users = random.sample(users, k=random.randint(1, min(5, len(users))))
        
        for user in selected_users:
            incident_worker = IncidentWorkerSchema(
                id=str(user['_id']), 
                name=user['name'],
                surname=user['surname'],
                type=None
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

        Incident.insert_one(fake_incident.model_dump())

    return "Success"

@app.get("/init/create_fake_comments", tags=["Initial"])
async def create_fake_comments():
    for _ in range(200):  
        users = list(User.find())

        selected_users = random.choice(users)

        incidents = list(Incident.find())

        selected_incident = random.choice(incidents)        

        fake_comment = CommentBaseSchema(
            incident_id=ObjectId(selected_incident["_id"]),
            created_by=ObjectId(selected_users["_id"]),
            created_at=datetime.now(),
            text=faker.sentence(),
        )

        Comment.insert_one(fake_comment.model_dump())

    return "Success"

@app.post("/api/auth/login", tags=["Authentication"])
def user_login(login_data: UserLoginSchema = Body(default=None)):
    if login_data:
        user = User.find_one(login_data.model_dump())
        if user:
            return {
                "name": user["name"],
                "surname": user["surname"],
                "is_admin": user["is_admin"],
                "token": signJWT(str(user['_id']))
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid login!")
    else:
        raise HTTPException(status_code=400, detail="No user data provided!")
                
@app.get("/api/users", response_model=List[UserSchema], tags=["Users"], dependencies=[Depends(jwtBearer())])
def users_list():
    users = User.find()
    return [{**user, "id": str(user["_id"])} for user in users]

@app.post("/api/users", response_model=UserSchema, tags=["Users"], dependencies=[Depends(jwtBearer())])
def create_user(new_user_data: UserCreateSchema = Body(default=None)):
    insert_result = User.insert_one(new_user_data.model_dump())
    new_user = User.find_one({"_id": insert_result.inserted_id})
    new_user['id'] = str(new_user['_id'])
    return new_user

@app.put("/api/users/{user_id}", response_model=UserSchema, tags=["Users"], dependencies=[Depends(jwtBearer())])
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

@app.delete("/api/users/{user_id}", tags=["Users"], dependencies=[Depends(jwtBearer())])
async def delete_user(user_id: str):
    deleted_user = User.delete_one({"_id": ObjectId(user_id)})
    if deleted_user.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@app.get("/api/users/types", response_model=List[UserTypeSchema], tags=["Users"], dependencies=[Depends(jwtBearer())])
async def users_types_list():
    user_types = UserType.find()
    return [{**user_type, "id": str(user_type["_id"])} for user_type in user_types]

@app.get("/api/incidents", response_model=List[IncidentSchema], tags=["Incidents"]) #, dependencies=[Depends(jwtBearer())]
async def incidents_list():
    incidents = Incident.find()
    
    incidents = sorted(incidents, key=lambda x: x["open_from"], reverse=True)
    
    return [{**incident, "id": str(incident["_id"])} for incident in incidents]

@app.post("/api/incidents", response_model=IncidentSchema, tags=["Incidents"], dependencies=[Depends(jwtBearer())])
async def create_incident(incident_data: IncidentBaseSchema = Body(default=None)):
    insert_result = Incident.insert_one(incident_data.model_dump())
    inserted_incident = Incident.find_one({"_id": insert_result.inserted_id})
    inserted_incident['id'] = str(inserted_incident['_id'])
    return inserted_incident

@app.put("/api/incidents/{id}", response_model=IncidentSchema, tags=["Incidents"], dependencies=[Depends(jwtBearer())])
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

@app.get("/api/incidents/{id}", response_model=IncidentSchema, tags=["Incidents"], dependencies=[Depends(jwtBearer())])
async def incident_get(id: str):
    existing_incident = Incident.find_one({"_id": ObjectId(id)})
    
    if existing_incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    return IncidentSchema(id=str(existing_incident['_id']), **existing_incident)

@app.delete("/api/incidents/{id}", tags=["Incidents"])
async def delete_incident(id: str):
    deleted_incident = Incident.delete_one({"_id": ObjectId(id)})
    if deleted_incident.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Incident not found")
    return {"message": "Incident deleted successfully"}

@app.get("/api/workers", response_model=List[IncidentWorkerSchema], tags=["Incidents"])
async def incident_workers_list():
    workers = User.find()
    return [{**worker, "id": str(worker["_id"])} for worker in workers]

@app.get("/api/incidents/{id}/comments", response_model=List[CommentDisplaySchema], tags=["Comments"], dependencies=[Depends(jwtBearer())])
async def comments_list(id: str):
    comments = list(Comment.find({"incident_id": ObjectId(id)}))
    
    comments = sorted(comments, key=lambda x: x["created_at"], reverse=True)

    processed_comments = []

    for i in comments:
        user = User.find_one({"_id": ObjectId(i["created_by"])})

        if not user:
            continue
        
        comment_data = {
            "id": i["_id"], 
            "created_by": user["name"] + " " + user["surname"], 
            "created_at": i["created_at"], 
            "text": i["text"]
        }
        
        processed_comments.append(comment_data)

    return processed_comments

@app.post("/api/incidents/{incident_id}/comments", response_model=CommentDisplaySchema, tags=["Comments"], dependencies=[Depends(jwtBearer())])
async def create_comment(incident_id: str, comment: CommentCreateSchema = Body(...), current_user_id: str = Depends(jwtBearer().get_current_user_id)):
    print(current_user_id)
    if not ObjectId.is_valid(incident_id):
        raise HTTPException(status_code=400, detail="Invalid incident ID")
    
    incident_obj_id = ObjectId(incident_id)
    
    incident = Incident.find_one({"_id": incident_obj_id})
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    user = User.find_one({"_id": ObjectId(current_user_id)})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    comment_data = {
        "incident_id": incident_obj_id,
        "created_by": ObjectId(user["_id"]),
        "created_at": datetime.now(),
        "text": comment.text
    }

    result = Comment.insert_one(comment_data)

    comment_data["_id"] = result.inserted_id
    
    user = User.find_one({"_id": ObjectId("665ca98f59fd56cbbb1c07f9")})
    
    comment_data["created_by"] = user["name"] + " " + user["surname"]

    return comment_data

@app.put("/api/incidents/{incident_id}/comments/{id}", response_model=CommentDisplaySchema, tags=["Comments"], dependencies=[Depends(jwtBearer())])
async def update_comment(incident_id: str, id: str, data: CommentCreateSchema):
    if not ObjectId.is_valid(incident_id):
        raise HTTPException(status_code=400, detail="Invalid incident ID")
    
    incident_obj_id = ObjectId(incident_id)
    
    incident = Incident.find_one({"_id": incident_obj_id})
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    comment_obj_id = ObjectId(id)
    
    comment = Comment.find_one({"_id": comment_obj_id})
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    Comment.update_one(
        {"_id": ObjectId(id)},
        {"$set": data.model_dump()},
    )
        
    comment["id"] = comment["_id"]
    comment["text"] = data.text
    
    user = User.find_one({"_id": ObjectId("665ca98f59fd56cbbb1c07f9")})
    
    comment["created_by"] = user["name"] + " " + user["surname"]

    return comment

@app.delete("/api/incidents/{incident_id}/comments/{id}", tags=["Comments"])
async def delete_comment(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid comment ID")

    deleted = Comment.delete_one({"_id": ObjectId(id)})
    
    if deleted.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    return {"message": "Comment deleted successfully"}