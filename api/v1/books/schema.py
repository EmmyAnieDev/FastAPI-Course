import uuid
from datetime import datetime, date
from typing import List, Optional

from pydantic import BaseModel

from api.v1.reviews.schema import ReviewModel


class BookModel(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date  # Changed from str to date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enables ORM mode for Pydantic v2


class BookDetailModel(BookModel):
    reviews: List[ReviewModel] = []

    class Config:
        from_attributes = True  # Enables ORM mode for Pydantic v2


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: date  # Changed from str to date
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str