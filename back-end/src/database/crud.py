from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.database.database import SessionLocal
from src.database.models import User, Gem
from src.database.schemas import UserCreate, Result


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(username: str):
    return SessionLocal().query(User).filter(User.name == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    # return db.query(models.User).offset(skip).limit(limit).all()
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email, name=user.name, mobile=user.mobile, password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def save_result(db: Session, result: Result, user_id: int):
    db_result = Gem(
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


def delete_result(db: Session, result_id: int):
    gem = db.get(Gem, result_id)
    if not gem:
        raise HTTPException(status_code=404, detail="Result not found")
    db.delete(gem)
    db.commit()
    return {"success": True}


def get_results(db: Session, user_id: int):
    return db.query(Gem).filter(Gem.user_id == user_id).all()
