from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import model, schemas

app = FastAPI()  # Create an instance of FastAPI

model.base.metadata.create_all(engine)


my_posts = [
    {"id": 1, "title": "Hello World", "content": "This is my first blog post"},
    {"id": 2, "title": "Second Post", "content": "This is my second blog post"},
]


# Decorator to define the path of the endpoint # response_model=List[schemas.Post]
@app.get("/", response_model=List[schemas.Post])
def read_post(db: Session = Depends(get_db)):
    posts = db.query(model.Posts).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = model.Posts(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):

    post = db.query(model.Posts).filter(model.Posts.id == post_id).first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found any post with the given {post_id}",
        )
    return post


@app.delete("/posts/{post_id}", response_model=schemas.Post)
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


@app.put("/posts/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(model.Posts).filter(model.Posts.id == post_id)
    updated_post = post_query.first()
    if updated_post == None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Post not found with the given Id {post_id}",
        )
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
