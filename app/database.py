from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:tayyab@localhost/person", echo=True)

base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
