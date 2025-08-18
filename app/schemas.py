from typing import Annotated, Optional
from datetime import datetime
from random import randrange

from pydantic import BaseModel, EmailStr




class BasePost(BaseModel):
    """Model representing a post."""
    Title: str
    Content: str
    Published: bool = True
    likes: Optional[int] = randrange(0, 10000)
    created_by: datetime = datetime.now()


class CreatePost(BaseModel):
    """Model representing a post."""
    Title: str
    Content: str
    Published: bool = True
    likes: Optional[int] = randrange(0, 10000)
    created_by: datetime = datetime.now()


class Update(BaseModel):
    """Model representing a post."""
    Title: str
    Content: str
    Published: bool = True
    likes: Optional[int] = randrange(0, 10000)
    created_by: datetime = datetime.now()


class Post(BaseModel):
    """Model representing a post."""
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
    
    Title: str
    Content: str
    # class Config:
    #     from_attributes = True
    #     allow_population_by_field_name = True
    #     fields = {
    #         "title": "Title",
    #         "content": "Content",
    #     }
    
    
class UserBase(BaseModel):
    """Model representing a user."""
    Name: str
    Email: EmailStr
    Password: int = randrange(0, 5000000)
    Created_at: datetime = datetime.now()
    
    
class CreateUser(BaseModel):
    """Model representing a user."""
    Name: str
    Email: EmailStr
    Password: str
    Created_at: datetime = datetime.now()
    

class UpdateUser(BaseModel):
    """Model representing a user."""
    Name: str
    Email: EmailStr
    Password: str
    Created_at: datetime = datetime.now()
    
    
class User(BaseModel):
    """Model representing a user."""
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
    
    Name: str
    Email: EmailStr
    
    