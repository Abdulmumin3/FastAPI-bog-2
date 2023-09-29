# The above code defines two Pydantic models, `Post` and `PostUpdate`, for representing blog posts
# with various fields and validation rules.
from pydantic import BaseModel, Field
from typing import Optional, List
# The above class is a subclass of BaseModel.
from datetime import datetime



class PostBase(BaseModel):
    title: str
    body: str
    published: Optional[bool]
    created_at: datetime = Field(..., format="%Y-%m-%d %H:%M:%S UTC")
    updated_at: datetime = Field(..., format="%Y-%m-%d %H:%M:%S UTC")
    
    # class Config():
    #     orm_mode=True

class Post(PostBase):
    class Config():
        orm_mode=True


class PostUpdate(BaseModel):
    title: str = Field(default="(Updated)")
    body: str
    published: Optional[bool]
    updated_at: datetime = Field(..., format="%Y-%m-%d %H:%M:%S UTC")
    
    class Config():
        orm_mode=True

class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    posts: List[Post] = []
    
    class Config():
        orm_mode=True
        
class GetPost(BaseModel):
    title: str
    body: str
    published: Optional[bool]
    created_at: datetime 
    updated_at: datetime
    author: ShowUser
    
    class Config():
        orm_mode=True