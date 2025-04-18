import uuid
from datetime import datetime, date
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field, Column, Relationship
from typing import Optional, List

from api.v1.auth import models
from api.v1.reviews.models import Review


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4()
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    user: Optional["models.User"] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(back_populates="book", sa_relationship_kwargs={"lazy": "selectin"})


    def __str__(self):
        return f"<Book {self.title}>"