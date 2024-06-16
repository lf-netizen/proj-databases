import os
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Path, Query
from sqlmodel import Session, select

from models.address import Address, AddressUpdate
from models.user import User
from clients.postgres import get_session

ROUTE_NAME = os.path.basename(__file__).replace(".py", "")

router = APIRouter(prefix=f"/{ROUTE_NAME}", tags=[ROUTE_NAME])


@router.post("/", response_model=Address)
def create_address(address_data: Address, user_id: int | None = Query(None, alias="user"), session: Session = Depends(get_session)):
    session.add(address_data)
    session.commit()
    session.refresh(address_data)

    if user_id:
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user.address_id = address_data.id
        session.commit()

    session.refresh(address_data)
    return address_data


@router.get("/", response_model=List[Address])
def read_addresses(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    return session.exec(select(Address).offset(skip).limit(limit)).all()


@router.get("/{address_id}", response_model=Address)
def read_address(address_id: int, session: Session = Depends(get_session)):
    address = session.get(Address, address_id)
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.put("/{address_id}", response_model=Address)
def update_address(address_id: int, address_data: Address, session: Session = Depends(get_session)):
    address = session.get(Address, address_id)
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")

    for field, value in address_data.model_dump(exclude_unset=True).items():
        setattr(address, field, value)

    session.commit()
    session.refresh(address)

    return address


@router.patch("/{address_id}", response_model=Address)
def patch_address(address_id: int, address_data: AddressUpdate, session: Session = Depends(get_session)):
    address = session.get(Address, address_id)
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")

    for field, value in address_data.model_dump(exclude_unset=True).items():
        setattr(address, field, value)

    session.commit()
    session.refresh(address)

    return address


@router.delete("/{address_id}", response_model=Address)
def delete_address(address_id: int, session: Session = Depends(get_session)):
    address = session.get(Address, address_id)
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    session.delete(address)
    session.commit()
    return address
