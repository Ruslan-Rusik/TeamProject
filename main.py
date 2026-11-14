from fastapi import FastAPI, Request, Form, Depends
from database.user import User, Base
from sqlalchemy.ext.asyncio import AsyncSession
from config.routes.routes import user_router, product_router, order_router
from config.database_config.config import get_db, engine
from config.fastapi_config.fastapi_config import templates
from contextlib import asynccontextmanager
from sqlalchemy import select
import product.endpoints.endpoints, user.endpoints.endpoints as apps

@asynccontextmanager
async def startup(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

app = FastAPI(lifespan=startup)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)

@app.get('/')
async def main(request: Request):
    return templates.TemplateResponse(request, name='main_page.html')