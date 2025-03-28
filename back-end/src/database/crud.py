import models
import schemas
from sqlalchemy.orm import Session
from database import SessionLocal


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(username: str):
    return (
        SessionLocal().query(models.User).filter(models.User.name == username).first()
    )


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    # return db.query(models.User).offset(skip).limit(limit).all()
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email, name=user.name, mobile=user.mobile, password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def save_result(db: Session, result: schemas.Result, user_id: int):
    db_result = models.Gem(
        name=result.filename,
        result=result.result,
        user_id=user_id,
        gem_type=result.gem_type,
        satisfactory=result.satisfactory,
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def get_results(db: Session, user_id: int):
    return db.query(models.Gem).filter(models.Gem.user_id == user_id).all()
