from typing import Optional, List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import model, schemas, utill, oauth

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", response_model=schemas.UserOut)
def user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(model.Users).filter(model.Users.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the {user_id} does not exists",
        )
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = utill.hash(user.password)
    user.password = hashed_password
    new_user = model.Users(**user.model_dump())
    print("Query", new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
