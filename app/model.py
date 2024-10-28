from sqlalchemy import String, Integer, Boolean, Column, text
from typing import Optional
from pydantic import BaseModel
from .database import base, engine, SessionLocal
from sqlalchemy.types import TIMESTAMP


class Posts(base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default="TRUE")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
