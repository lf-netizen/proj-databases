from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import requests
import aiohttp
from nanoid import generate


app = FastAPI()
base_url = "http://api:8000"

class Product(BaseModel):
    id: str = Field(default_factory=lambda: generate(size=10))
    name: str
    description: str = "default description"
    sell_price: float = 0
    quantity: int = 0
    buy_price: float = 0
    date: str
    image_id: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    is_enabled: bool = True

@app.get("/products", response_model=List[Product])
async def get_products():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base_url}/products/") as response:
            products = await response.json()
            return [Product(**product) for product in products]
    # return requests.get(f"{base_url}/products/")

@app.get("/product/{product_id}", response_model=Product)
async def get_product(product_id: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base_url}/products/{product_id}") as response:
            return await response.json()
    # product = next((product for product in products_db if product["id"] == product_id), None)
    # if product is None:
    #     raise HTTPException(status_code=404, detail="Product not found")
    # return product

@app.put("/product/{product_id}", response_model=Product)
async def update_product(product_id: str, updated_product: Product):
    async with aiohttp.ClientSession() as session:
        async with session.put(f"{base_url}/products/{product_id}", json=updated_product.dict()) as response:
            
            return await response.json()
            # if product_index is None:
            #     raise HTTPException(status_code=404, detail="Product not found")
            # products_db[product_index] = updated_product.dict()
            # return updated_product
            # return await response.json()

            # product_index = next((index for index, product in enumerate(products_db) if product["id"] == product_id), None)
            # if product_index is None:
            #     raise HTTPException(status_code=404, detail="Product not found")
            # products_db[product_index] = updated_product.dict()
            # return updated_product

