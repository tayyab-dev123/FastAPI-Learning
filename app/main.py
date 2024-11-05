from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import model, schemas, utill
from .routers import user, post, auth

app = FastAPI()  # Create an instance of FastAPI

model.base.metadata.create_all(engine)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
