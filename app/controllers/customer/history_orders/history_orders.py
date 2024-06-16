from fastapi import FastAPI, HTTPException, Request
import csv
import os
import requests
from typing import Dict

app = FastAPI()


# Endpoint do pobierania historii zamówień
@app.get("/orders/{user}")
async def get_order_history(user: str):
    response = requests.get("http://api:8000/orders",
                            params=dict(user=user)).json()
    if not response:
        raise HTTPException(status_code=404, detail="Orders not found")

    for order in response[-20:]:
        cart_items = [
            item
            for item in requests.get(f"http://api:8000/carts/{order['cart_id']-1}/items").json()
        ]
        order['products'] = [
            requests.get(
                f"http://api:8000/products/{item['product_id']}").json() | dict(quantity=item['quantity'])
            for item in cart_items
        ]
    return response[-20:]


# Endpoint do przyjmowania opinii o produktach
@ app.post("/review")
def submit_review(request:Dict):
    user_id = request.get("user_id")
    product_id = request.get("product_id")
    content = request.get("content")
    if not user_id or not product_id or not content :
        raise HTTPException(status_code=400, detail="Incomplete review data")
    try:
        requests.post('http://api:8000/opinions/',json={'user_id':user_id, "product_id": product_id,
                                                        "content": content})
        return {"message": "Review submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    
