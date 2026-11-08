from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Category, Product, Seller
from config.database_config.config import get_db
from fastapi import Depends, HTTPException
from product.schema.schemas import CategoryOut, CategoryIn, CategoryOutWithProducts, ProductIn, ProductOut
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from config.routes.routes import product_router


@product_router.post('/api/create_category', response_model=CategoryOut)
async def create_category(category: CategoryIn, session: AsyncSession = Depends(get_db)):
    new_category = Category(name=category.name)

    session.add(new_category)

    await session.commit()

    await session.refresh(new_category)

    return new_category

@product_router.get('/api/get_categories/', response_model=List[CategoryOut])
async def get_categories(session: AsyncSession = Depends(get_db)):
    stmt = select(Category)

    result = await session.execute(stmt)

    categories = result.scalars().all()

    return categories

@product_router.get('/api/get_category/{idx}', response_model=CategoryOutWithProducts)
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

@product_router.post('/api/create_product/', response_model=ProductOut)
async def create_product(product: ProductIn, session: AsyncSession = Depends(get_db)):
    stmt = (
        select(Seller)
        .where(Seller.id == product.seller_id)
    )

    result = await session.execute(stmt)

    seller = result.scalar_one_or_none()

    if seller is None:
        raise HTTPException(
            status_code=404,
            detail='Seller is not found'
        )

    stmt = (
        select(Category)
        .where(Category.id == product.category_id)
    )

    result = await session.execute(stmt)

    category = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(
            status_code=404,
            detail='Category is not found'
        )

    if product.stock < 0:
        raise HTTPException(
            status_code=400,
            detail='Stock cannot be negative'
        )

    if product.price < 0:
        raise HTTPException(
            status_code=400,
            detail='Price cannot be negative'
        )

    new_product = Product(
        name=product.name,
        description=product.description,
        stock=product.stock,
        price=product.price,
        seller_id=product.seller_id,
        category_id=product.category_id
    )

    session.add(new_product)

    await session.commit()

    await session.refresh(new_product)

    return new_product



@product_router.get('/api/get_products/', response_model=List[ProductOut])
async def get_products(session: AsyncSession = Depends(get_db)):
    stmt = select(Product)

    result = await session.execute(stmt)

    products = result.scalars().all()

    return products



@product_router.get('/api/get_product/{idx}', response_model=ProductOut)
async def get_product(idx: int, session: AsyncSession = Depends(get_db)):
    stmt = (
        select(Product)
        .where(Product.id == idx)
    )

    result = await session.execute(stmt)

    product = result.scalar_one_or_none()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail='Product is not found'
        )

    return product















