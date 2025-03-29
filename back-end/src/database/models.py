from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from src.database.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    mobile = Column(String(255), unique=True)
    password = Column(String(255))


class Gem(Base):
    __tablename__ = "gems"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    gem_type = Column(String(255))
    result = Column(Enum("heated", "natural", "synthetic"))
    satisfactory = Column(Enum("satisfied", "unsatisfied", "neutral"))
    user_id = Column(Integer, ForeignKey("users.id"))


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
