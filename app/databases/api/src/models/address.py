from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class Address(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    street: str
    city: str
    postal_code: str

    user: Optional["User"] = Relationship(back_populates="address")


class AddressUpdate(BaseModel):
    name: str | None = None
    street: str | None = None
    city: str | None = None
    postal_code: str | None = None
