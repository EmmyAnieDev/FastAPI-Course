from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text
from sqlmodel import SQLModel

from config import Config

# Creates an asynchronous database engine using the provided database URL, with SQL statement logging enabled.
engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)


async def init_db():
    async with engine.begin() as conn:  # Open an async database connection
        await conn.run_sync(SQLModel.metadata.create_all)  # Create all database tables based on defined models