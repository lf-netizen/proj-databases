import os
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.order import Order, OrderUpdate
from clients.postgres import get_session

ROUTE_NAME = os.path.basename(__file__).replace(".py", "")

router = APIRouter(prefix=f"/{ROUTE_NAME}", tags=[ROUTE_NAME])


@router.post("/", response_model=Order)
def create_order(order: Order, session: Session = Depends(get_session)):
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


@router.get("/", response_model=List[Order])
def read_orders(user: str = Query(default=None), session: Session = Depends(get_session)):
    statement = select(Order)
    if user:
        statement = statement.filter(Order.user_id == user)
    return session.exec(statement).all()


@router.delete("/", status_code=200)
def delete_orders(session: Session = Depends(get_session)):
    statement = select(Order)
    orders = session.exec(statement).all()
    for order in orders:
        session.delete(order)
    session.commit()
    return {"detail": "All orders deleted successfully"}


@ router.get("/{order_id}", response_model=Order)
def read_order(order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@ router.put("/{order_id}", response_model=Order)
def update_order(order_id: int, order: Order, session: Session = Depends(get_session)):
    existing_order = session.get(Order, order_id)
    if existing_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    for field, value in order.model_dump(exclude_unset=True).items():
        setattr(existing_order, field, value)

    session.commit()
    session.refresh(existing_order)

    return existing_order


@ router.patch("/{order_id}", response_model=Order)
def patch_order(order_id: int, order_update: OrderUpdate, session: Session = Depends(get_session)):
    existing_order = session.get(Order, order_id)
    if existing_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    for field, value in order_update.dict(exclude_unset=True).items():
        setattr(existing_order, field, value)

    session.commit()
    session.refresh(existing_order)

    return existing_order


@ router.delete("/{order_id}", response_model=Order)
def delete_order(order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    session.delete(order)
    session.commit()
    return order
