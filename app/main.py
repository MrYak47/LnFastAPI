"""Module providing a function printing python version."""

# from typing import Annotated, List
# from datetime import datetime, timezone
# from random import randrange

# from sqlmodel import SQLModel, Field, Session, create_engine, select
# from contextlib import asynccontextmanager
# import psycopg
# from psycopg.rows import dict_row
from fastapi import FastAPI
# , Response, status, HTTPException, Depends
# import fastapi.params as params

# from . import models, utils, schemas
# from .schemas import CreatePost, Update, CreateUser, UpdateUser
# from .database import engine, get_session, create_db_and_tables
from .routers import posts, users

app = FastAPI()

# try:
#     conn = psycopg.connect(
#         host="localhost",
#         port=5432,
#         dbname="fastapiDb",
#         user="postgres",
#         password="Dyslpostgres",
#         row_factory=dict_row
#         )
#     print("Connected to the database successfully.")
# except psycopg.OperationalError as e:
#     print(f"Error connecting to the database: {e}")

app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(users.router, prefix="/users", tags=["Users"])




@app.get("/")
async def root():
    """Root endpoint that returns a simple greeting message."""
    return {"message": "Hello, FastAPI!"}


