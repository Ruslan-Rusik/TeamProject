from pydantic import BaseModel, ConfigDict
from typing import List, Any



class CategoryBase(BaseModel):
    name: str

class CategoryIn(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class CategoryOutWithProducts(CategoryOut):
    products: List[Any]