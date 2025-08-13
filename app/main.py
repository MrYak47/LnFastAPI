"""Module providing a function printing python version."""

from datetime import datetime
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, Response, status, HTTPException
# import fastapi.params as params
from pydantic import BaseModel



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



app = FastAPI()

@app.get("/")
async def root():
    """Root endpoint that returns a simple greeting message."""
    return {"message": "Hello"}


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
    for post in my_post:
        if post['id'] == post_id:
            return {"data": post}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"error": "Post not found"}, 404

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    """Endpoint to delete a post by its ID."""
    for index, post in enumerate(my_post):
        if post['id'] == post_id:
            del my_post[index]
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )

@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: Post):
    """Endpoint to update a post by its ID."""
    for index, existing_post in enumerate(my_post):
        if existing_post['id'] == post_id:
            updated_post = post.model_dump()
            updated_post['id'] = post_id
            my_post[index] = updated_post
            return {"data": updated_post}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )

