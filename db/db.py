from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from config import Config

# Creates an asynchronous database engine using the provided database URL, with SQL statement logging enabled.
engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)


async def init_db():
    async with engine.begin() as conn:  # Open an async database connection

        await conn.run_sync(SQLModel.metadata.create_all)  # Create all database tables based on defined models


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session  # Provide the session to be used in dependency injection