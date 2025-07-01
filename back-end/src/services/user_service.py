import os
import base64
from datetime import timedelta
import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.database import crud, schemas
from src.utils import jwtService
from fastapi import HTTPException

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
IMG_PATH = "data/test"  # Define image path constant


async def get_user_by_email(db: Session, email: str):
    """Fetches a user by their email address."""
    try:
        return crud.get_user_by_email(db, email=email)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="A database error occurred while Fetching User By Email",
        )


async def create_user(db: Session, user: schemas.UserCreate):
    """Hashes the password and creates a new user."""
    try:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)
        user.password = hashed_password.decode("utf-8")
        return crud.create_user(db=db, user=user)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="A database error occurred while Creating User",
        )


async def login_for_access_token(db: Session, email: str, password: str):
    """Verifies user credentials and returns a JWT access token."""
    try:
        db_user = crud.get_user_by_email(db, email=email)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="A database error occurred while Fetching User By Email",
        )
    if not db_user or not bcrypt.checkpw(
        password.encode("utf-8"), db_user.password.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwtService.create_access_token(
        data={"sub": db_user.email, "id": db_user.id},
        expires_delta=access_token_expires,
    )
    return access_token, db_user


async def save_classification_result(db: Session, result: schemas.Result, user_id: int):
    """Saves a classification result to the database for a specific user."""
    try:
        return crud.save_result(db=db, result=result, user_id=user_id)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="A database error occurred while Saving Classification Result",
        )


def _encode_image_to_base64(image_path: str):
    """Encodes an image file to a Base64 string if it exists."""
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def get_user_history_with_images(db: Session, user_id: int):
    """Retrieves all results for a user and attaches the corresponding image data."""
    try:
        results = crud.get_results(db=db, user_id=user_id)
        for res in results:
            image_path = os.path.join(IMG_PATH, res.name)
            res.image = _encode_image_to_base64(image_path)
        return results
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="A database error occurred.")
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while fetching history.",
        )


async def delete_history_record(db: Session, result_id: int):
    try:
        return crud.delete_result(db, result_id)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="A database error occurred while deleting a history record",
        )
