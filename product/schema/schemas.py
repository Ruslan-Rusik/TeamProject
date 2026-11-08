from pydantic import BaseModel, ConfigDict
from typing import List, Any
from decimal import Decimal



class CategoryBase(BaseModel):
    name: str

class CategoryIn(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class CategoryOutWithProducts(CategoryOut):
    products: List['ProductOut']

class ProductBase(BaseModel):
    name: str
    description: str
    stock: int
    price: Decimal

    seller_id: int
    category_id: int

class ProductIn(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)