from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from database.user import User, Buyer, Seller
from config.database_config.config import get_db
from ..schema.schemas import UserResponse, UserCreate, UserRole
from config.routes.routes import user_router



@user_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user_in.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Эмейл уже зарегистрирован"
        )

    new_user = User(username=user_in.username, email=user_in.email)
    db.add(new_user)
    await db.flush()

    if user_in.role == UserRole.BUYER:
        new_buyer = Buyer(user_id=new_user.id)
        db.add(new_buyer)
    elif user_in.role == UserRole.SELLER:
        new_seller = Seller(user_id=new_user.id)
        db.add(new_seller)

    await db.commit()
    await db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "role": user_in.role
    }


@user_router.get("/", response_model=List[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    if not users:
        return []

    sellers_res = await db.execute(select(Seller.user_id))
    seller_user_ids = set(sellers_res.scalars().all())

    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": UserRole.SELLER if user.id in seller_user_ids else UserRole.BUYER,
        }
        for user in users
    ]


@user_router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Юзер не найден"
        )

    seller_res = await db.execute(select(Seller).filter(Seller.user_id == user_id))
    role = UserRole.SELLER if seller_res.scalars().first() else UserRole.BUYER

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": role
    }