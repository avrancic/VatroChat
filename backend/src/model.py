from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class UserTypeBaseSchema(BaseModel):
    type: str = Field(default = None)
    
class UserTypeSchema(UserTypeBaseSchema):
    id: str

    class Config:
        from_attributes = True

class UserBaseSchema(BaseModel):
    name: str = Field(default = None)
    surname: str = Field(default = None)
    username: str = Field(default = None)
    type: UserTypeSchema | None = None
    is_admin: bool = Field(default = False)

class UserCreateSchema(UserBaseSchema):
    password: str

class UserSchema(UserBaseSchema):
    id: str

    class Config:
        from_attributes = True

class UserLoginSchema(BaseModel):
    username: str = Field(default = None)
    password: str = Field(default = None)

class IncidentsSchema(BaseModel):
    description: str = Field(default = None)
    users: Optional[List[UserSchema]] = None
    active: bool = Field(default = True)

class ShiftsBaseSchema(BaseModel):
    users: List[UserSchema] = []
    from_time: datetime = Field(default = None)
    to_time: datetime = Field(default = None)
    
class ShiftsSchema(ShiftsBaseSchema):
    id: str

    class Config:
        from_attributes = True