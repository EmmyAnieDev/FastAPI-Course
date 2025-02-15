from typing import List
from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from api.v1.books.models import Book
from api.v1.books.schema import BookUpdateModel, BookCreateModel
from api.v1.books.service import BookService
from db.db import get_session

book_router = APIRouter()
book_service = BookService()



@book_router.get('/', response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@book_router.get('/{book_id}', response_model=Book)
async def get_book(book_id: str, session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book(book_id, session)

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

    return book


@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session)) -> dict:
    new_book = await book_service.create_a_book(book_data, session)
    return new_book


@book_router.patch('/{book_id}', status_code=status.HTTP_200_OK, response_model=Book)
async def update_book(book_id: str, book_update_data: BookUpdateModel, session: AsyncSession = Depends(get_session)) -> dict:
    updated_book = await book_service.update_book(book_id, book_update_data, session)

    if updated_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

    return updated_book


@book_router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, session: AsyncSession = Depends(get_session)):
    success = await book_service.delete_book(book_id, session)

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

    return {}