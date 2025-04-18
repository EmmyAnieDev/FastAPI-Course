import uuid
from datetime import datetime

from fastapi import Depends
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import Book
from .schema import BookCreateModel, BookUpdateModel


class BookService:


    @staticmethod
    async def get_all_books(session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()


    @staticmethod
    async def get_user_books( user_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.user_uid == user_uid).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()


    @staticmethod
    async def get_book(book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        return book if book is not None else None


    @staticmethod
    async def get_user_book(book_uid: str, user_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.user_uid == user_uid).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        return book if book is not None else None


    @staticmethod
    async def create_a_book(book_data: BookCreateModel, user_uid: str, session: AsyncSession):
        book_data_dict = book_data.model_dump()  # Convert to dictionary
        new_book = Book(**book_data_dict, uid=uuid.uuid4(), created_at=datetime.now(), updated_at=datetime.now())
        new_book.user_uid = user_uid
        new_book.published_date = datetime.strptime(book_data_dict['published_date'], '%Y-%m-%d')
        session.add(new_book)
        await session.commit()
        return new_book


    async def update_book(self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_book(book_uid, session)
        if book_to_update is None:
            return None

        update_data_dict = update_data.model_dump(exclude_unset=True)  # Exclude unset fields

        # Iterate through the update_data_dict and update each field of the book instance
        for k, v in update_data_dict.items():
            setattr(book_to_update, k, v)  # Dynamically update the book's attributes with new values

        book_to_update.updated_at = datetime.now()

        await session.commit()
        await session.refresh(book_to_update)  # Refresh to get updated data
        return book_to_update


    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)
        if book_to_delete is None:
            return None

        await session.delete(book_to_delete)
        await session.commit()
        return True