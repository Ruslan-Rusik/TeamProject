from config.database_config.config import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from order import Order
    from product import Product



class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    buyer: Mapped['Buyer'] = relationship(back_populates='user', uselist=False)
    seller: Mapped['Seller'] = relationship(back_populates='user', uselist=False)

    def __repr__(self) -> str:
        return f"""
            Username: {self.username}
            \nEmail: {self.email}
        """

class Buyer(Base):
    __tablename__ = 'buyers'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True, unique=True)

    user: Mapped['User'] = relationship(back_populates='buyer')
    orders: Mapped[List['Order']] = relationship(back_populates='buyer')

    def __repr__(self) -> str:
        return f"""
            Buyer
            \n{self.user}
        """

class Seller(Base):
    __tablename__ = 'sellers'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True, unique=True)

    user: Mapped['User'] = relationship(back_populates='seller')
    products: Mapped[List['Product']] = relationship(back_populates='seller')

    def __repr__(self) -> str:
        return f"""
            Seller
            \n{self.user}
        """

















