from fastapi import FastAPI,Request
# from config.routes.routes import user_router
from contextlib import asynccontextmanager
from config.database_config.config import engine
from config.database_config.config import Base
import user.endpoints.endpoints

# короче костыль на ордер
import sys
from types import ModuleType

import database.models

if not hasattr(database.models, "Order"):

    class Order:
        pass

    database.models.Order = Order
#========================

@asynccontextmanager
async def startup(app:FastAPI):
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=startup)
# app.include_router(user_router)

@app.get("/")
async def main_page(request:Request):
    return []