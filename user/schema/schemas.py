from pydantic import BaseModel
from enum import Enum


class UserRole(str, Enum):
    BUYER = "buyer"
    SELLER = "seller"


class UserCreate(BaseModel):
    username: str
    email: str
    role: UserRole


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole

    class Config:
        from_attributes = True