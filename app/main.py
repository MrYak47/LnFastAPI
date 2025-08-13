"""Module providing a function printing python version."""

from typing import Annotated, Optional
from datetime import datetime
from random import randrange
from contextlib import asynccontextmanager
import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, Response, status, HTTPException, Depends
# import fastapi.params as params
from pydantic import BaseModel
from . import models
from .database import engine, get_session, create_db_and_tables
from sqlmodel import SQLModel, Field, Session, create_engine, select




class Post(BaseModel):
    """Model representing a post."""
    title: str
    content: str
    published: bool = True
    likes: Optional[int] = randrange(0, 10000)
    created_by: datetime = datetime.now()

try:
    conn = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="fastapiDb",
        user="postgres",
        password="Dyslpostgres",
        row_factory=dict_row
        )
    print("Connected to the database successfully.")
except psycopg.OperationalError as e:
    print(f"Error connecting to the database: {e}")

my_post = [{
            "id": 1, 
            "title": "title of post ", 
            "content": "content of post", 
            "published": True,
            "likes": 200
            },
           {
            "id": 2, "title": 
            "favorurite foods", 
            "content": "banana, berries, apples", 
            "published": False,
            "likes": 500
            }
           ]


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler to create database tables."""
    create_db_and_tables()
    yield
    # Cleanup actions can be added here if needed

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    """Root endpoint that returns a simple greeting message."""
    return {"message": "Hello"}


@app.get("/sqlmodel")
async def test_posts(session: SessionDep):
    """Endpoint to test SQLModel posts."""
    statement = select(models.Post)
    results = session.exec(statement).all()
    return {"data": results}


@app.get("/posts")
async def getposts():
    """Root endpoint that returns a simple greeting message."""
    # Example of using psycopg3 connection directly
    with psycopg.connect(dbname="fastapiDb", user="postgres", password="Dyslpostgres") as db_conn:
        with db_conn.cursor() as cur:
            cur.execute("""SELECT * FROM public."Posts" """)
            posts = cur.fetchall()
            print(posts)
    return {"data":posts}


@app.post("/create", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    """Endpoint to create a post."""
    likes = post.likes if post.likes is not None else randrange(0, 10000)
    with psycopg.connect(dbname="fastapiDb", user="postgres", password="Dyslpostgres") as db_conn:
        with db_conn.cursor() as cur:
            cur.execute("""INSERT INTO public."Posts"("Title", "Content", "Published", "Likes")
                        VALUES(%s, %s, %s, %s) RETURNING *""",
                        (post.title, post.content, post.published, likes))
            postnew = cur.fetchone()
            db_conn.commit()
    return {"data": "Post created successfully"}


@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    """Endpoint to retrieve a post by its ID."""
    with psycopg.connect(dbname="fastapiDb", user="postgres", password="Dyslpostgres") as db_conn:
        with db_conn.cursor() as cur:
            cur.execute("""SELECT * FROM public."Posts" WHERE "Id" = %s """, (str(post_id),))
            post = cur.fetchone()
            if not post :
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found"
                )
            return {"data": post}
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"error": "Post not found"}, 404


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    """Endpoint to delete a post by its ID."""
    with psycopg.connect(dbname="fastapiDb", user="postgres", password="Dyslpostgres") as db_conn:
        with db_conn.cursor() as cur:
            cur.execute("""DELETE FROM public."Posts" WHERE "Id" = %s RETURNING *""", (str(post_id),))
            del_post = cur.fetchone()
            db_conn.commit()
            if not del_post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found"
                )
            return {"data": del_post}


@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: Post):
    """Endpoint to update a post by its ID."""
    likes = post.likes if post.likes is not None else randrange(0, 10000)
    with psycopg.connect(dbname="fastapiDb", user="postgres", password="Dyslpostgres") as db_conn:
        with db_conn.cursor() as cur:
            cur.execute("""UPDATE public."Posts" 
                        SET "Title" = %s, "Content" = %s, "Published" = %s, "Likes" = %s
                        WHERE "Id" = %s
                        RETURNING *""", (post.title, post.content, post.published, likes, str(post_id))
                        )
            updated_post = cur.fetchone()
            db_conn.commit()

            if update_post is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found"
                )
            return {"data": updated_post}

