from fastapi import FastAPI, HTTPException
from typing import List
import requests
from pydantic import BaseModel

from config import Product

###
# WAREHOUSE
# backend for warehouse operations e.g. restock
###

app = FastAPI()
api_url = "http://api:8000"


# get all products
@app.get("/products/", response_model=List[Product])
def get_products():
    response = requests.get(f'{api_url}/products')
    return [Product(**product) for product in response.json()]


# get only products with quantity lower than treshold
@app.get("/products/low_stock/{threshold}", response_model=List[Product])
def get_low_stock_products(threshold: int):
    products = get_products()
    return [product for product in products if product.quantity < threshold]


# helper class for @app.post below
class Stock(BaseModel):
    additional_stock : int

# restock product given bought batch
@app.post("/products/restock/{product_id}", response_model=Product)
def restock_product(product_id: str, additional_stock: Stock):
    response = requests.get(f"{api_url}/products/{product_id}")
    product_to_restock = Product(**response.json())
    product_to_restock.quantity += additional_stock.additional_stock
    response = requests.put(f"{api_url}/products/{product_id}", json=product_to_restock.dict())
    return response
