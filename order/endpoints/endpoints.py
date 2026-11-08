from database.order import OrderItem, Order

from fastapi import Request,Form, Depends, HTTPException, status

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from config.routes.routes import order_router
from order.schema.schema import OrderCresate, OrderItemCreate, OrderItem,OrderResponce

from config.database_config.config import get_db


@order_router.get("/", name="orders:all_orders")
async def get_orders(request:Request, session:AsyncSession=Depends(get_db)):
    res = await session.execute(select(Order))
    orders = res.scalars().all()
    if not orders:
        return []
    context = {"orders": orders}
    return context


@order_router.post("/", response_model=OrderResponce,status_code=status.HTTP_201_CREATED)
async  def create_order(order_data=OrderCresate, session:AsyncSession=Depends(get_db)):
    ...