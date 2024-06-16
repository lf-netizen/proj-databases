from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class Cart(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True)

    items: List["CartItem"] = Relationship(back_populates="cart")


class CartItem(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: str
    quantity: int
    cart_id: Optional[int] = Field(default=None, foreign_key="cart.id")

    cart: Cart = Relationship(back_populates="items")
