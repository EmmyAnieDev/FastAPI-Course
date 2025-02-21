from typing import List
from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from api.v1.auth.dependency import AccessTokenBearer, CheckRole
from api.v1.books.models import Book
from api.v1.books.schema import BookUpdateModel, BookCreateModel
from api.v1.books.service import BookService
from db.db import get_session

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(CheckRole(['admin', 'user']))


@book_router.get('/', response_model=List[Book], dependencies=[role_checker])
async def get_all_books(session: AsyncSession = Depends(get_session), user_detail=Depends(access_token_bearer)):
    books = await book_service.get_all_books(session)
    return books


@book_router.get('/{book_id}', response_model=Book, dependencies=[role_checker])
async def get_book(book_id: str, session: AsyncSession = Depends(get_session), user_detail=Depends(access_token_bearer)):
    book = await book_service.get_book(book_id, session)

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

    return book


@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=Book, dependencies=[role_checker])
async def create_a_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session), user_detail=Depends(access_token_bearer)) -> dict:
    new_book = await book_service.create_a_book(book_data, session)
    return new_book


@book_router.patch('/{book_id}', status_code=status.HTTP_200_OK, response_model=Book, dependencies=[role_checker])
async def update_book(book_id: str, book_update_data: BookUpdateModel, session: AsyncSession = Depends(get_session), user_detail=Depends(access_token_bearer)) -> dict:
    updated_book = await book_service.update_book(book_id, book_update_data, session)

    if updated_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

    return updated_book


@book_router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(book_id: str, session: AsyncSession = Depends(get_session), user_detail=Depends(access_token_bearer)):
    success = await book_service.delete_book(book_id, session)

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

    return {}