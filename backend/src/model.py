from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {
            "type": "string",
            "format": "objectid"
        }

class UserTypeBaseSchema(BaseModel):
    name: str = None
    
class UserTypeSchema(UserTypeBaseSchema):
    id: str

    class Config:
        from_attributes = True

class UserBaseSchema(BaseModel):
    name: str = None
    surname: str = None
    username: str = None
    type: Optional[UserTypeSchema] = None
    is_admin: bool = False

class UserCreateSchema(UserBaseSchema):
    password: str

class UserUpdateSchema(UserBaseSchema):
    password: Optional[str]

class UserSchema(UserBaseSchema):
    id: str

    class Config:
        from_attributes = True

class UserLoginSchema(BaseModel):
    username: str = Field(default = None)
    password: str = Field(default = None)

class IncidentWorkerSchema(BaseModel):
    id: str
    name: str
    surname: str 
    type: Optional[UserTypeSchema] = None

class IncidentBaseSchema(BaseModel):
    title: str = None
    location: str = None
    open_from: datetime = Field(default_factory=datetime.now)
    open_until: Optional[datetime] = None
    workers: Optional[List[IncidentWorkerSchema]] = None
    
    class Config:
        json_encoders = {ObjectId: str}

class IncidentSchema(IncidentBaseSchema):
    id: str

    class Config:
        from_attributes = True

class CommentBaseSchema(BaseModel):
    incident_id: PyObjectId
    created_by: PyObjectId  # Reference to a user
    created_at: datetime = Field(default_factory=datetime.now)
    text: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}

class CommentSchema(CommentBaseSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="id")

    class Config:
        from_attributes = True

class CommentCreateSchema(BaseModel):
    text: str

class CommentDisplaySchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="id")
    created_by: str  # Reference to a user
    created_at: datetime
    text: str
    
    class Config:
        json_encoders = {ObjectId: str}