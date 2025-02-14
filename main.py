from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Path parameter: Retrieves the name from the URL path
@app.get('/greet/{name}')
async def greet_name(name: str) -> dict:
    return {"message": f"Hello {name}"}


# Query parameter: Retrieves the name from the query string (e.g., /show?name=Tommy)
@app.get('/show')
async def show_name(name: str) -> dict:
    return {"message": f"Hello {name}"}


# Mixed parameters: Retrieves name from the path and age from the query string
# (e.g., /details/Tommy/?age=25)
@app.get('/details/{name}')
async def details(name: str, age: int) -> dict:
    return {"message": f"Hello {name}, you're {age} years old"}


# Query parameters with default values (name defaults to "User", age defaults to 0)
# (e.g., /person/?name=Tommy&age=25)
@app.get('/person')
async def person(name: str = "User", age: int = 0) -> dict:
    return {"name": name, "age": age}


class BookCreateModel(BaseModel):   # Inheriting from Base Model class.
    author: str
    title: str


@app.post('/create_book')
async def create_book(book_data: BookCreateModel):  # book_data is an instance of BookCreateModel
    return {
        "author": book_data.author,
        "title": book_data.title
    }