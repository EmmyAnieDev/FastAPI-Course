from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text

from config import Config

# Creates an asynchronous database engine using the provided database URL, with SQL statement logging enabled.
engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)


async def init_db():
    async with engine.begin() as conn:
        statement = text("SELECT 'hello';")
        result = await conn.execute(statement)
        print(result.fetchall())