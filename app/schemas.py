from typing import Annotated, Optional
from datetime import datetime
from random import randrange

from pydantic import BaseModel




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