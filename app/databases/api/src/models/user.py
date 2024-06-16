from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    password: str
    is_admin: bool

    address_id: int | None = Field(default=None, foreign_key="address.id")
    cart_id: int | None = Field(default=None, foreign_key="cart.id")

    address: Optional["Address"] = Relationship(back_populates="user")
    cart: Optional["Cart"] = Relationship(
        sa_relationship_kwargs=dict(foreign_keys="[User.cart_id]"))


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    is_admin: bool | None = None

    address_id: int | None = None
    cart_id: int | None = None
