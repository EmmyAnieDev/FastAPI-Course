from typing import List
from fastapi import status, APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from api.v1.auth.dependency import AccessTokenBearer, CheckRole
from api.v1.books.models import Book
from api.v1.books.schema import BookUpdateModel, BookCreateModel, BookDetailModel
from api.v1.books.service import BookService
from db.db import get_session

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(CheckRole(['admin', 'user']))


# GET all books existing in DB
@book_router.get('/', response_model=List[BookDetailModel], dependencies=[role_checker])
async def get_all_books(session: AsyncSession = Depends(get_session), token_details=Depends(access_token_bearer)):
    books = await book_service.get_all_books(session)
    return books


# GET all books submitted by a user
@book_router.get('/user/{user_uid}', response_model=List[BookDetailModel], dependencies=[role_checker])
async def get_user_book_submissions(user_uid: str, session: AsyncSession = Depends(get_session), token_details=Depends(access_token_bearer)):
    books = await book_service.get_user_books(user_uid, session)
    return books


# Get book
@book_router.get('/{book_id}', response_model=BookDetailModel, dependencies=[role_checker])
async def get_book(book_id: str, session: AsyncSession = Depends(get_session), token_details=Depends(access_token_bearer)):
    book = await book_service.get_book(book_id, session)

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

    return book


# Get book for a specific user
@book_router.get('/{book_id}/user/{user_id}', response_model=BookDetailModel, dependencies=[role_checker])
async def get_book(book_id: str, session: AsyncSession = Depends(get_session), token_details=Depends(access_token_bearer)):
    user_uid = token_details['user']['user_uid']
    book = await book_service.get_user_book(book_id, user_uid, session)

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

    return book


@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=BookDetailModel, dependencies=[role_checker])
async def create_a_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session), token_details=Depends(access_token_bearer)) -> dict:
    user_uid = token_details['user']['user_uid']
    new_book = await book_service.create_a_book(book_data, user_uid, session)
    return new_book


@book_router.patch('/{book_id}', status_code=status.HTTP_200_OK, response_model=BookDetailModel, dependencies=[role_checker])
async def update_book(book_id: str, book_update_data: BookUpdateModel, session: AsyncSession = Depends(get_session), token_details=Depends(access_token_bearer)) -> dict:
    updated_book = await book_service.update_book(book_id, book_update_data, session)

    if updated_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

    return updated_book


@book_router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(book_id: str, session: AsyncSession = Depends(get_session), token_details=Depends(access_token_bearer)):
    success = await book_service.delete_book(book_id, session)

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")

    return {}