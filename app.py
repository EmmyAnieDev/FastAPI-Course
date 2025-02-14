from typing import List
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel


app = FastAPI()


class InMemoryDB:
    books = [
        {
            "id": 1,
            "title": "Atomic Habits",
            "author": "James Clear",
            "publisher": "Penguin Random House",
            "published_date": "2018-10-16",
            "page_count": 320,
            "language": "English"
        },
        {
            "id": 2,
            "title": "The Alchemist",
            "author": "Paulo Coelho",
            "publisher": "HarperOne",
            "published_date": "1988-04-15",
            "page_count": 208,
            "language": "English"
        },
        {
            "id": 3,
            "title": "Deep Work",
            "author": "Cal Newport",
            "publisher": "Grand Central Pub",
            "published_date": "2016-01-05",
            "page_count": 304,
            "language": "English"
        },
        {
            "id": 4,
            "title": "The Pragmatic Programmer",
            "author": "Andy Hunt, Dave Thomas",
            "publisher": "Addison-Wesley",
            "published_date": "1999-10-30",
            "page_count": 352,
            "language": "English"
        },
        {
            "id": 5,
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "publisher": "Prentice Hall",
            "published_date": "2008-08-01",
            "page_count": 464,
            "language": "English"
        },
        {
            "id": 6,
            "title": "Rich Dad Poor Dad",
            "author": "Robert Kiyosaki",
            "publisher": "Plata Publishing",
            "published_date": "1997-04-01",
            "page_count": 336,
            "language": "English"
        },
        {
            "id": 7,
            "title": "The Lean Startup",
            "author": "Eric Ries",
            "publisher": "Crown Business",
            "published_date": "2011-09-13",
            "page_count": 336,
            "language": "English"
        },
        {
            "id": 8,
            "title": "Zero to One",
            "author": "Peter Thiel",
            "publisher": "Crown Business",
            "published_date": "2014-09-16",
            "page_count": 224,
            "language": "English"
        },
        {
            "id": 9,
            "title": "The Phoenix Project",
            "author": "Gene Kim, Kevin Behr, George Spafford",
            "publisher": "IT Revolution Press",
            "published_date": "2013-01-10",
            "page_count": 432,
            "language": "English"
        },
        {
            "id": 10,
            "title": "Cracking the Coding Interview",
            "author": "Gayle Laakmann McDowell",
            "publisher": "CareerCup",
            "published_date": "2015-07-01",
            "page_count": 687,
            "language": "English"
        }
    ]


class BookModel(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str


db = InMemoryDB()


@app.get('/books', response_model=List[BookModel])
async def get_all_books():
    return db.books


@app.get('/books/{book_id}')
async def get_book(book_id: int):

    for book in db.books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")


@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: BookModel) -> dict:
    new_book = book_data.model_dump()

    db.books.append(new_book)

    return {"Message": "New Book Created", "book": new_book, "status_code": 201}


@app.patch('/books/{book_id}', status_code=status.HTTP_200_OK)
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


@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):

    for book in db.books:
        if book["id"] == book_id:
            db.books.remove(book)

            return {}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")