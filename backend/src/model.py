from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

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

class IncidentSchema(IncidentBaseSchema):
    id: str

    class Config:
        from_attributes = True

class CommentBaseSchema(BaseModel):
    incident_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    text: Optional[str] = None

class CommentSchema(CommentBaseSchema):
    id: str

    class Config:
        from_attributes = True
