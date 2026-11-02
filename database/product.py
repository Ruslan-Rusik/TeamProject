from config.database_config.config import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Numeric, ForeignKey
from decimal import Decimal
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from user import Seller
    from order import OrderItem



class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    products: Mapped[List['Product']] = relationship(back_populates='category')

    def __repr__(self) -> str:
        return f"""
            Name: {self.name}
        """

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    seller_id: Mapped[int] = mapped_column(ForeignKey('sellers.id'), index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), index=True)

    seller: Mapped['Seller'] = relationship(back_populates='products')
    category: Mapped['Category'] = relationship(back_populates='products')
    order_items: Mapped[List['OrderItem']] = relationship(back_populates='product')

    def __repr__(self) -> str:
        return f"""
            Name: {self.name}
            \nDescription: {self.description}
            \nCategory: {self.category}
            \nSeller: {self.seller.user}
        """



