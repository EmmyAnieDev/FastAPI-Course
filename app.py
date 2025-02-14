from fastapi import FastAPI

from api.books.v1.routes import book_router

version = 'v1'

app = FastAPI(
    title="FastAPI Course",
    description="A REST API for a book review web service",
    version=version
)

app.include_router(book_router, prefix=f'/api/{version}/books', tags=['books'])