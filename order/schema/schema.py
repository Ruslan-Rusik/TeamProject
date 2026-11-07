from pydantic import BaseModel, Field
from decimal import Decimal




class OrderItem(BaseModel):
    product_id: int
    count: int  = Field(..., description="Count of products")
    price: Decimal = Field(..., description="Price")


class OrderResponce(OrderItem):
    id: int
    total_price: Decimal

    class Config:
        from_attributes = True
