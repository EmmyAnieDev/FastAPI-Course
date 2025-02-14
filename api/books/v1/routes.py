from typing import List
from fastapi import status, APIRouter
from fastapi.exceptions import HTTPException

from api.books.v1.book_data import InMemoryDB
from api.books.v1.schema import BookModel, BookUpdateModel

book_router = APIRouter()
db = InMemoryDB()


@book_router.get('/', response_model=List[BookModel])
async def get_all_books():
    return db.books


@book_router.get('/{book_id}')
async def get_book(book_id: int):

    for book in db.books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")


@book_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: BookModel) -> dict:
    new_book = book_data.model_dump()

    db.books.append(new_book)

    return {"Message": "New Book Created", "book": new_book, "status_code": 201}


@book_router.patch('/{book_id}', status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book_update_data: BookUpdateModel) -> dict:

    for book in db.books:
        if book["id"] == book_id:
            book['title'] = book_update_data.title
            book['author'] = book_update_data.author
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language

            return {"Message": "Book Updated", "book": book, "status_code": 200}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")


@book_router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):

    for book in db.books:
        if book["id"] == book_id:
            db.books.remove(book)

            return {}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")