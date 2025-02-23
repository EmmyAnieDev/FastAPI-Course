import uuid
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from api.v1.books.models import Book


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)   # Exclude from Serialization
    created_at: datetime
    updated_at: datetime
    books: List[Book]


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=50)
    password: str = Field(min_length=8)


class UserLoginModel(BaseModel):
    email: str = Field(max_length=50)
    password: str = Field(min_length=8)