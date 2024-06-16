from sqlmodel import SQLModel, Field
from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


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


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cart_id: int = Field(foreign_key="cart.id")
    user_id: int = Field(foreign_key="user.id")
    address_id: int = Field(foreign_key="address.id")
    date: str = Field(
        default_factory=lambda: datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    status: str
    total_amount: float

# class OrderStatus(str, Enum):
#     PLACED = "placed"
#     DONE = "done"

class OrderUpdate(BaseModel):
    cart_id: Optional[int] = None
    user_id: Optional[int] = None
    date: Optional[str] = None
    status: Optional[str] = None
    total_amount: Optional[float] = None
