from pydantic import BaseModel, Field
from datetime import datetime

class UserTypeSchema(BaseModel):
    type: str = Field(default = None)

class UserBaseSchema(BaseModel):
    name: str = Field(default = None)
    surname: str = Field(default = None)
    username: str = Field(default = None)
    type: list[UserTypeSchema] | None = None
    is_admin: bool = Field(default = False)

class UserCreateSchema(UserBaseSchema):
    password: str

class UserSchema(UserBaseSchema):
    id: str

    class Config:
        from_attributes = True

class IncidentsSchema(BaseModel):
    description: str = Field(default = None)
    users: list[UserSchema] | None = None
    active: bool = Field(default = True)

class ShiftsSchema(BaseModel):
    users: list[UserSchema] | None = None
    from_time: datetime = Field(default = None)
    to_time: datetime = Field(default = None)

class UserLoginSchema(BaseModel):
    username: str = Field(default = None)
    password: str = Field(default = None)