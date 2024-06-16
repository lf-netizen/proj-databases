from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum


class OrderStatus(Enum):
    """
    Enumeration for representing all statuses an order can have.

    Attributes:
        PENDING (str): Order has been created but not processed.
        PROCESSING (str): Order is being processed.
        PACKAGING (str): Order is being packaged.
        SHIPPED (str): Order has been shipped.
        DELIVERED (str): Order has been delivered.
        CANCELLED (str): Order has been cancelled.
        RETURNED (str): Order has been returned.
    """
    PENDING = "pending"
    PROCESSING = "processing"
    PACKAGING = "packaging"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"


class Order(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True)
    cart_id: int = Field(foreign_key="cart.id")
    user_id: int = Field(foreign_key="user.id")
    address_id: int = Field(foreign_key="address.id")
    date: str = Field(default_factory=lambda: datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    status: str
    total_amount: float


class Cart(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True)

    items: List["CartItem"] = Relationship(back_populates="cart")


class CartItem(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: str
    quantity: int
    cart_id: Optional[int] = Field(default=None, foreign_key="cart.id")

    cart: Cart = Relationship(back_populates="items")
