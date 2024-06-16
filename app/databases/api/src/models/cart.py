from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from typing import List


class Cart(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    items: List["CartItem"] = Relationship(back_populates="cart")


class CartItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: str
    quantity: int
    cart_id: int | None = Field(default=None, foreign_key="cart.id")

    cart: Cart = Relationship(back_populates="items")


class CartUpdate(BaseModel):
    pass


class CartItemUpdate(BaseModel):
    product_id: str | None = None
    quantity: int | None = None
