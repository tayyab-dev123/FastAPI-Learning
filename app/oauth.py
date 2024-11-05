from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from . import schemas, model
from .database import get_db
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

# SECRET KEY
# ALGORITHM
# EXPIRATION TIME
SECRET_KEY = "bf803d72ad818f2cf7efc891ca3d6a62b7f92bb10309f203283d77ac34ee5e50fc790c7918b6562801f565d4a3c413c9719d7717f746b5d86fa0a8af97f15203"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 60


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to verify credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)
    user = db.query(model.Users).filter(model.Users.id == token.id).first()

    return user
