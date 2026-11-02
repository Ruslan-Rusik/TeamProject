from config.database_config.config import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Numeric, ForeignKey
from decimal import Decimal
from typing import List, TYPE_CHECKING
from datetime import datetime, UTC

if TYPE_CHECKING:
    from product import Product
    from user import Buyer



class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), index=True)
    count: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), index=True)

    order: Mapped['Order'] = relationship(back_populates='order_items')
    product: Mapped['Product'] = relationship(back_populates='order_items')

    def __repr__(self):
        return f"""
            \nProduct: {self.product.name}
            \nCount: {self.count}
            \nTotal price: {self.total_price}
            \nBuyer: {self.order.buyer.user}
            \nSeller: {self.product.seller.user}
        """

class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)

    buyer_id: Mapped[int] = mapped_column(ForeignKey('buyers.id'), index=True)

    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    dt: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    buyer: Mapped['Buyer'] = relationship(back_populates='orders')
    order_items: Mapped[List['OrderItem']] = relationship(back_populates='order')

    def __repr__(self):
        return f"""
            Items: {self.order_items}
            \ndt: {self.dt}
        """