from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Literal

class PostBase(BaseModel):  #Validates every field in the Class, and tries to convert first, if the conversion to a set datatype fails it will errors.
    title: str
    content: str
    published: bool = True #if left empty it will default to True. (optional field)
    #rating: int | None = None # # Optional field, accepts an int or None (Union type)

class PostCreate(PostBase):
    pass

class Post(PostBase): # <<-- this is a response schema.
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel): # <-- Response model for users. SO it doesn't return the password.
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None

class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]

class PostOut(BaseModel):
    Post: Post
    votes: int

    model_config = ConfigDict(from_attributes=True)
