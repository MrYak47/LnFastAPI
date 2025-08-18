"""This file is part of the FastAPI application for managing users."""
from typing import Annotated, List
from datetime import datetime, timezone
from random import randrange

from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
# import fastapi.params as params
from sqlmodel import Session, select
from app import models, utils, schemas
from app.schemas import CreateUser, UpdateUser
from app.database import get_session, create_db_and_tables

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler to create database tables."""
    create_db_and_tables()
    yield
    # Cleanup actions can be added here if needed

app = FastAPI(lifespan=lifespan)

@router.get("/Users", response_model=List[schemas.User])
async def getusers(session: SessionDep):
    """Root endpoint that returns all users."""

    statement = select(models.User)
    results = session.exec(statement).all()
    
    return results


@router.post("/createUser", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(user: CreateUser, session: SessionDep):
    """Endpoint to create a user."""


    hashed_password = utils.hash(user.Password)
    user.Password = hashed_password
    new_user = models.User(
        Name=user.Name,
        Email=user.Email,
        Created_at=user.Created_at if user.Created_at is not None else datetime.now(timezone.utc),
        Password=user.Password
    )

    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.get("/User/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, session: SessionDep):
    """Endpoint to retrieve a user by its ID."""
    
    statement = select(models.User).where(models.User.Id == user_id)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    
    
    
    return user



@router.delete("/User_del/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: SessionDep):
    """Endpoint to delete a user by its ID."""
    
    statement = select(models.User).where(models.User.Id == user_id)
    result = session.exec(statement)
    user = result.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    print(user)
    session.delete(user)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/User_Up/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: UpdateUser, session: SessionDep):
    """Endpoint to update a user by its ID."""
    
    up_user = session.get(models.User, user_id)
   
    if not up_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    
    up_user.Name = user.Name
    up_user.Email = user.Email
    up_user.Password = user.Password if user.Password is not None else randrange(0, 5000000)
    
    print(up_user)
    session.add(up_user)
    session.commit()
    session.refresh(up_user)
    return up_user

