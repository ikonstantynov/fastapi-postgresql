import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    username: str
    email: EmailStr

    class Config:
        arbitrary_types_allowed = True


class UserCreate(UserBase):
    register_date: datetime = Field(default_factory=datetime.now)
    password: str


class UserUpdate(BaseModel):
    password: str


class UserInDBBase(UserBase):
    register_date: datetime = Field(default_factory=datetime.now)


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
