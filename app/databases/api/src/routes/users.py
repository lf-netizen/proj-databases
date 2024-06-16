import os
from typing import List
from fastapi import APIRouter, HTTPException, Query, Depends, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from urllib.parse import urlencode

from models.user import User, UserUpdate

from clients.postgres import get_session


ROUTE_NAME = os.path.basename(__file__).replace(".py", "")

router = APIRouter(prefix=f"/{ROUTE_NAME}", tags=[ROUTE_NAME])


@router.post("/", response_model=User)
def create_user(user_data: User, session: Session = Depends(get_session)):
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data


@router.get("/", response_model=List[User])
def read_users(username: str | None = Query(None), session: Session = Depends(get_session)):
    statement = select(User)
    if username:
        statement = statement.where(User.username == username)
    return session.exec(statement).all()


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_data: User, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    session.commit()
    session.refresh(user)
    return user


@ router.patch("/{user_id}", response_model=User)
def patch_user(user_id: int, user_data: UserUpdate, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    session.commit()
    session.refresh(user)
    return user


@ router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()

    return user


@router.get("/{user_id}/cart")
@router.post("/{user_id}/cart")
@router.put("/{user_id}/cart")
@router.patch("/{user_id}/cart")
@router.delete("/{user_id}/cart")
def redirect_to_user_cart(user_id: int, request: Request, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if request.method == "POST":
        params = dict(user=user_id)
        return RedirectResponse(url=f"/carts?{urlencode(params)}", status_code=307)
    elif user.cart_id:
        return RedirectResponse(url=f"/carts/{user.cart_id}", status_code=307)
    else:
        raise HTTPException(
            status_code=404, detail="User does not have a cart")


@router.get("/{user_id}/cart/items")
@router.post("/{user_id}/cart/items")
def redirect_to_cart_items(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.cart_id:
        return RedirectResponse(url=f"/carts/{user.cart_id}/items", status_code=307)
    else:
        raise HTTPException(
            status_code=404, detail="User does not have a cart")


@router.get("/{user_id}/cart/items/{item_id}")
@router.put("/{user_id}/cart/items/{item_id}")
@router.patch("/{user_id}/cart/items/{item_id}")
@router.delete("/{user_id}/cart/items/{item_id}")
def redirect_to_cart_item(user_id: int, item_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.cart_id:
        return RedirectResponse(url=f"/carts/{user.cart_id}/items/{item_id}", status_code=307)
    else:
        raise HTTPException(
            status_code=404, detail="User does not have a cart")


@router.get("/{user_id}/address")
@router.post("/{user_id}/address")
@router.put("/{user_id}/address")
@router.patch("/{user_id}/address")
@router.delete("/{user_id}/address")
def redirect_to_user_address(user_id: int, request: Request, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if request.method == "POST":
        params = dict(user=user_id)
        return RedirectResponse(url=f"/addresses?{urlencode(params)}", status_code=307)
    elif user.address_id:
        return RedirectResponse(url=f"/addresses/{user.address_id}", status_code=307)
    else:
        raise HTTPException(
            status_code=404, detail="User does not have an address")
