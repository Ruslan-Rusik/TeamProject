from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession



Base = declarative_base()

# DATABASE_URL = 'sqlite+aiosqlite:///./shop.db'
DATABASE_URL = "mysql+aiomysql://database_admin:qwerty123@db:3306/fastapi_practice"

engine = create_async_engine(
    url=DATABASE_URL
)

session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with session() as s:
        yield s