from fastapi import APIRouter

from routes import (
    products,
    orders,
    users,
    carts,
    addresses,
    files,
    opinions,
)


router = APIRouter()

router.include_router(products.router)
router.include_router(orders.router)
router.include_router(users.router)
router.include_router(carts.router)
router.include_router(addresses.router)
router.include_router(files.router)
router.include_router(opinions.router)
