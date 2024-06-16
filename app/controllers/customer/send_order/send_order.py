from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime
import requests
import logging
from typing import Optional, List
from enum import Enum

app = FastAPI()

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

class OrderDb(BaseModel):
    cart_id: int
    user_id: int
    address_id: int
    date: str = Field(
        default_factory=lambda: datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    status: str
    total_amount: float


class Address(BaseModel):
    id: Optional[int] = None
    name: str
    street: str
    city: str
    postal_code: str


class CartItem(BaseModel):
    product_id: str
    quantity: int


class Order(BaseModel):
    first_name: str
    last_name: str
    address: str
    city: str
    postal_code: str
    email: str
    payment_method: str
    user_id: int
    total_amount: float

@app.post("/submit_order/")
async def submit_order(order: Order):
    address = Address(
        name=f"{order.first_name} {order.last_name}",
        street=order.address,
        city=order.city,
        postal_code=order.postal_code,
    )
    response = requests.post("http://api:8000/addresses",
                             json=address.model_dump()).json()
    address_id = response.get('id')

    response = requests.post(f"http://api:8000/users/{order.user_id}").json()
    if 'cart_id' not in response:
        response = requests.post(
            f"http://api:8000/users/{order.user_id}/cart", json={}).json()
        cart_id = response.get('id')
    else:
        cart_id = response.get('cart_id')

    items = requests.get(
        f"http://api:8000/carts/{cart_id}/items").json()
    products = [
        requests.get(f"http://api:8000/products/{item['product_id']}").json()
        for item in items
    ]

    missing_quantity = [
        product['name']
        for item, product in zip(items, products)
        if item['quantity'] > product['quantity']
    ]

    if missing_quantity:
        return JSONResponse(
            status_code=522,
            content=f"The following products are missing: {missing_quantity}"
        )

    # total_amount = round(sum(item['quantity'] * product['sell_price']
    #                    for item, product in zip(items, products)),2)
    dborder = OrderDb(
        status="PENDING",
        total_amount=order.total_amount,
        address_id=address_id,
        user_id=order.user_id,
        cart_id=cart_id,
    )
    print(dborder.model_dump())
    response = requests.post("http://api:8000/orders",
                             json=dborder.model_dump())
    

    return dict(message="OK")


@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    logging.error(f"Validation error: {exc.body}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )
