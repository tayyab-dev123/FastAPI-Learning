from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import model

app = FastAPI()  # Create an instance of FastAPI

model.base.metadata.create_all(engine)


class Post(BaseModel):
    title: str
    content: str
    published: bool
    # rating: Optional[int] = None


my_posts = [
    {"id": 1, "title": "Hello World", "content": "This is my first blog post"},
    {"id": 2, "title": "Second Post", "content": "This is my second blog post"},
]


@app.get("/")  # Decorator to define the path of the endpoint
def read_root(db: Session = Depends(get_db)):
    posts = db.query(model.Posts).all()
    return {"Data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = model.Posts(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{post_id}")
def read_post(post_id: int, db: Session = Depends(get_db)):

    post = db.query(model.Posts).filter(model.Posts.id == post_id).first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found any post with the given {post_id}",
        )
    return {"Data": post}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(model.Posts).filter(model.Posts.id == post_id)
    print("Query", post)
    if post.first() == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Post not found with the given Id {post_id}",
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post, db: Session = Depends(get_db)):
    post_query = db.query(model.Posts).filter(model.Posts.id == post_id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Post not found with the given Id {post_id}",
        )
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return {"Data": post_query.first()}
