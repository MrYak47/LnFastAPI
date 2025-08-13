from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from . import models
# from  sqlalchemy.ext.declarative import declarative_base



DATABASE_URL = "postgresql://postgres:Dyslpostgres@localhost/fastapiDb"

engine = create_engine(DATABASE_URL)

SessionLocal = Session(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


def create_db_and_tables():
    models.SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

