"""This module defines the FastAPI router for handling posts-related operations.
It includes endpoints for creating, retrieving, updating, and deleting posts."""
from typing import Annotated, List
from datetime import datetime, timezone
from random import randrange

from contextlib import asynccontextmanager
# import psycopg
# from psycopg.rows import dict_row
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlmodel import Session, select

from app import models, schemas
from app.schemas import CreatePost, Update
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


@router.get("/")
async def root():
    """Root endpoint that returns a simple greeting message."""
    return {"message": "Hello"}


@router.get("/", response_model=List[schemas.Post])
async def getposts(session: SessionDep):
    """Root endpoint that returns all posts."""
    # Example of using psycopg3 connection directly
    # with psycopg.connect(dbname="fastapiDb", user="postgres", password="Dyslpostgres") as db_conn:
    #     with db_conn.cursor() as cur:
    #         cur.execute("""SELECT * FROM public."Posts" """)
    #         posts = cur.fetchall()
    #         print(posts)

    statement = select(models.Post)
    results = session.exec(statement).all()

    return results


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: CreatePost, session: SessionDep):
    """Endpoint to create a post."""
    likes = post.likes if post.likes is not None else randrange(0, 10000)
    # with psycopg.connect(dbname="fastapiDb", user="postgres", password="Dyslpostgres") as db_conn:
    #     with db_conn.cursor() as cur:
    #         cur.execute("""INSERT INTO public."Posts"("Title", "Content", "Published", "Likes")
    #                     VALUES(%s, %s, %s, %s) RETURNING *""",
    #                     (post.title, post.content, post.published, likes))
    #         postnew = cur.fetchone()
    #         db_conn.commit()
    

    new_post = models.Post(
        Title=post.Title,
        Content=post.Content,
        Published=post.Published,
        Likes=likes
    )

    
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@router.get("/{post_id}", response_model=schemas.Post)
async def get_post(post_id: int, session: SessionDep):
    """Endpoint to retrieve a post by its ID."""
    # with psycopg.connect(dbname="fastapiDb", user="postgres", password="Dyslpostgres") as db_conn:
    #     with db_conn.cursor() as cur:
    #         cur.execute("""SELECT * FROM public."Posts" WHERE "Id" = %s """, (str(post_id),))
    #         post = cur.fetchone()
    #         if not post :
    #             raise HTTPException(
    #                 status_code=status.HTTP_404_NOT_FOUND,
    #                 detail="Post not found"
    #             )
    #         return {"data": post}
    # response.status_code = status.HTTP_404_NOT_FOUND
    
    statement = select(models.Post).where(models.Post.Id == post_id)
    post = session.exec(statement).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post



@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, session: SessionDep):
    """Endpoint to delete a post by its ID."""
    # with psycopg.connect(dbname="fastapiDb", user="postgres", password="Dyslpostgres") as db_conn:
    #     with db_conn.cursor() as cur:
    #         cur.execute("""DELETE FROM public."Posts" WHERE "Id" = %s RETURNING *""",
    #           (str(post_id),))
    #         del_post = cur.fetchone()
    #         db_conn.commit()
    #         if not del_post:
    #             raise HTTPException(
    #                 status_code=status.HTTP_404_NOT_FOUND,
    #                 detail="Post not found"
    #             )
    #         return {"data": del_post}


    statement = select(models.Post).where(models.Post.Id == post_id)
    result = session.exec(statement)
    post = result.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    print(post)
    session.delete(post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{post_id}", response_model=schemas.Post)
async def update_post(post_id: int, post: Update, session: SessionDep):
    """Endpoint to update a post by its ID."""
    # likes = post.likes if post.likes is not None else randrange(0, 10000)
    # with psycopg.connect(dbname="fastapiDb", user="postgres", password="Dyslpostgres") as db_conn:
    #     with db_conn.cursor() as cur:
    #         cur.execute("""UPDATE public."Posts" 
    #                     SET "Title" = %s, "Content" = %s, "Published" = %s, "Likes" = %s
    #                     WHERE "Id" = %s
    #                     RETURNING *""", (post.title, post.content, post.published, likes, str(post_id))
    #                     )
    #         updated_post = cur.fetchone()
    #         db_conn.commit()

    #         if update_post is None:
    #             raise HTTPException(
    #                 status_code=status.HTTP_404_NOT_FOUND,
    #                 detail="Post not found"
    #             )
    #         return {"data": updated_post}

    up_post = session.get(models.Post, post_id)
   
    if not up_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    
    up_post.Title = post.title
    up_post.Content = post.content
    up_post.Published = post.published
    up_post.Likes = post.likes if post.likes is not None else randrange(0, 10000)
    
    print(up_post)
    session.add(up_post)
    session.commit()
    session.refresh(up_post)
    return up_post

