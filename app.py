from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.v1.auth.routes import auth_router
from api.v1.books.routes import book_router
from db.db import init_db


@asynccontextmanager
async def life_span(app:FastAPI):
    print('Server is starting ...')
    await init_db()
    yield
    print('Server has been stopped.')


version = 'v1'

app = FastAPI(
    title="FastAPI Course",
    description="A REST API for a book review web service",
    version=version,
    lifespan=life_span
)

app.include_router(book_router, prefix=f'/api/{version}/books', tags=['books'])
app.include_router(auth_router, prefix=f'/api/{version}/auth', tags=['users'])