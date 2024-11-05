from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

# database.py

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:<password>@localhost/<Database name>"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:tayyab@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
