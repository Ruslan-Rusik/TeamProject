from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List




class OrderItem(BaseModel):
    product_id: int
    count: int  = Field(..., description="Count of products")
    price: Decimal = Field(..., description="Price")


class OrderItemCreate(BaseModel):
    product_id:int
    count:int=Field(..., gt=0)

class OrderCresate(BaseModel):
    buyer_id:int
    items:List[OrderItemCreate]

class OrderResponce(OrderItem):
    id: int
    total_price: Decimal

    class Config:
        from_attributes = True
