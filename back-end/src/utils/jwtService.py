import jwt
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
from ..database import crud, database, models
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = ALGORITHM = os.getenv("ALGORITHM")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_token(token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("Token", token)
        payload = jwt.decode(
            token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_signature": False},
        )
        print("Payload", payload)
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = models.TokenData(email=email)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = crud.get_user_by_email(db=database.SessionLocal(), email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
