from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class UserTypeBaseSchema(BaseModel):
    type: Optional[str] = None
    
class UserTypeSchema(UserTypeBaseSchema):
    id: str

    class Config:
        from_attributes = True

class UserBaseSchema(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    username: Optional[str] = None
    type: Optional[UserTypeSchema] = None
    is_admin: bool = False

class UserCreateSchema(UserBaseSchema):
    password: str

class UserSchema(UserBaseSchema):
    id: str

    class Config:
        from_attributes = True

class UserLoginSchema(BaseModel):
    username: str = Field(default = None)
    password: str = Field(default = None)

class IncidentBaseSchema(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    open_from: datetime = Field(default_factory=datetime.now)
    open_until: Optional[datetime] = None
    workers: Optional[List[UserSchema]] = None

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