from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    ime: str = Field(default = None)
    prezime: str = Field(default = None)
    username: str = Field(default = None)
    password: str = Field(default = None)
    class Config:
        the_schema = {
            "user_demo" : {
            }
        }