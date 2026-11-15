from fastapi import APIRouter, Depends, HTTPException, status, FastAPI,Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from database.user import User, Buyer, Seller
from config.database_config.config import get_db
from config.fastapi_config.fastapi_config import templates
from config.routes.routes import user_router


@user_router.get("/users_page",name="users:users_page")
async def get_users(request:Request,session: AsyncSession = Depends(get_db)):
    res = await session.execute(select(User))
    users = res.scalars().all()
    context = {"users":users}
    return templates.TemplateResponse(request=request,name="user_template/user.html",context=context)