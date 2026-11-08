from fastapi import APIRouter

user_router = APIRouter(prefix='/users')
category_router = APIRouter(prefix='/categories')
product_router = APIRouter(prefix='/products')
order_router = APIRouter(prefix='/orders')
