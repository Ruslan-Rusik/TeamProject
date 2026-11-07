from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Category
from config.database_config.config import get_db
from fastapi import Depends, HTTPException
from product.schema.schemas import CategoryOut, CategoryIn, CategoryOutWithProducts
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import joinedload



@app.post('/api/create_category', response_model=CategoryOut)
async def create_category(category: CategoryIn, session: AsyncSession = Depends(get_db)):
    new_category = Category(name=category.name)

    session.add(new_category)

    await session.commit()

    await session.refresh(new_category)

    return new_category

@app.get('/api/get_categories/', response_model=List[CategoryOut])
async def get_categories(session: AsyncSession = Depends(get_db)):
    stmt = select(Category)

    result = await session.execute(stmt)

    categories = result.scalars().all()

    return categories

@app.get('/api/get_category/{idx}', response_model=CategoryOutWithProducts)
async def get_category(idx: int, session: AsyncSession = Depends(get_db)):
    stmt = (
        select(Category)
        .where(Category.id==idx)
        .options(
            joinedload(Category.products)
        )
    )

    result = await session.execute(stmt)

    category = result.unique().scalar_one_or_none()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail='Category is not found'
        )

    return category















