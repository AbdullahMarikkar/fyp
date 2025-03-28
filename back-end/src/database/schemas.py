from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str
    mobile: str
    password: str


class UserCreate(UserBase):
    pass


class UserLogIn(BaseModel):
    email: str
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_model = True


class Result(BaseModel):
    filename: str
    result: str
    satisfactory: str
    gem_type: str
