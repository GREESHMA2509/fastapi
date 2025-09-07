from pydantic import BaseModel,EmailStr,conint
from datetime import datetime
from typing import Optional
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
"""class CreatePost(BaseModel):
    title:str
    content:str
    published:bool=True
class UpdatePost(BaseModel):
    #title:str
    #content:str
    published:bool"""
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email:EmailStr
    class Config:
        form_attributes=True

class Post(PostBase):
    id:int
    #title:str
    #content:str
    #published:bool
    created_at:datetime
    owner_id:int
    owner:UserOut
    class Config:
        form_attributes=True
class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    access_type:str
class TokenData(BaseModel):
    id:Optional[str]=None
class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)

class PostOut(PostBase):
    Post:Post
    votes:int
