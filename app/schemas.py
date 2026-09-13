from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):  #Validates every field in the Class, and tries to convert first, if the conversion to a set datatype fails it will errors.
    title: str
    content: str
    published: bool = True #if left empty it will default to True. (optional field)
    #rating: int | None = None # # Optional field, accepts an int or None (Union type)

class PostCreate(PostBase):
    pass

class Post(PostBase): # <<-- this is a response schema.
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str