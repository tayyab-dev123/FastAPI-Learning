from sqlalchemy import String, Integer, Boolean, Column
from typing import Optional
from pydantic import BaseModel
from database import base, engine


def create_table():
    base.metadata.create_all(engine)


class Person(base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(40), nullable=False)
    lastname = Column(String(40), nullable=False)
    isMale = Column(Boolean)
