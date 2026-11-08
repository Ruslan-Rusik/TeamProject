from fastapi import FastAPI, Request, Form, Depends
from database.user import User, Base
from sqlalchemy.ext.asyncio import AsyncSession
from config.database_config.config import get_db, engine
from contextlib import asynccontextmanager
from sqlalchemy import select

app = FastAPI()


@asynccontextmanager  # Он нужен, чтобы закрыть функцию startup
async def startup(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


@app.get('/')
def test_db(session: AsyncSession = Depends(get_db)):
    result = await session.execute(
        select(User),
    )

    try:
        users = result.scalars().all()
        return {'users': users}
    except Exception:
        return {'users': "error"}
