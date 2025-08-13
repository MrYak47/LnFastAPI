from datetime import datetime, timezone
# from .database import Base
from random import randrange
from sqlalchemy import func, text
from sqlalchemy.types import DateTime
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, Column






class Post(SQLModel, table=True):
    """Model representing a post."""
    __tablename__ = "posts"
    
    id: int = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(nullable=False, max_length=100)
    content: str = Field(nullable=False, max_length=500)
    published: bool = Field(sa_column_kwargs={"server_default": str("False")})
    created_by: datetime =  Field(sa_column=Column(DateTime, nullable=True, server_default=text("(now() AT TIME ZONE 'UTC')")))
    likes: int = Field(default=randrange(0, 10000), nullable=True)