from datetime import datetime, timezone
# \from .database import Base
from random import randrange
from sqlalchemy import func, text
from sqlalchemy.types import DateTime
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, Column, Relationship






class Post(SQLModel, table=True):
    """Model representing a post."""
    __tablename__ = "Posts"

    Id: int = Field(default=None, primary_key=True, nullable=False)
    Title: str = Field(nullable=False, max_length=100)
    Content: str = Field(nullable=False, max_length=500)
    Published: bool = Field(sa_column_kwargs={"server_default": str("False")})
    Created_by: datetime =  Field(
        sa_column=Column(
            DateTime, nullable=True, server_default=text("(now() AT TIME ZONE 'UTC')")))
    Likes: int = Field(default=randrange(0, 10000), nullable=True)
    # user_id: int = Field(foreign_key="Users.Id", nullable=False)
    # User: "User" = Relationship(back_populates="Posts")


class User(SQLModel, table=True):
    """Model representing a user."""
    __tablename__ = "Users"

    Id: int = Field(default=None, primary_key=True, nullable=False)
    Name: str = Field(nullable=False, max_length=100)
    Email: str = Field(nullable=False, max_length=100)
    Password: str = Field(nullable=False, max_length=100)
    Created_at: datetime = Field(
        sa_column=Column(DateTime,
                            nullable=True,
                            server_default=text("(now() AT TIME ZONE 'UTC')")))
    # Posts: list[Post] = Relationship(back_populates ="User")
    

