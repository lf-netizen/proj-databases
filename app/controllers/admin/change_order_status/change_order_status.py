from fastapi import FastAPI, HTTPException
from typing import List
from config import Order, Cart, OrderStatus
import requests


app = FastAPI()
api_url = "http://api:8000"


def get_product(id:str,quantity:int):
    resp = requests.get(f"{api_url}/products/{id}")
    if resp.status_code == 200:
        item ={'name': resp.json().get('name'),
               'id': resp.json().get('id'),
               'sell_price': resp.json().get('sell_price'),
               'quantity': quantity}
        return item
    else:
        print(f'Failed to get your product: {id}')
    

# get all orders with given status
@app.get("/orders", response_model=List[Order])
def get_orders(order_status: str):
    response = requests.get(f'{api_url}/orders')
    if not response.status_code == 200:
        raise HTTPException(status_code=response.status_code, detail='ERROR')
    orders = [Order(**order) for order in response.json()]
    if order_status == 'all':
        return [order for order in orders]
    else:
        return [order for order in orders if order.status == order_status]



# Endpoint do pobierania historii zamówień
@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    response = requests.get(f"{api_url}/orders/{order_id}")
    if response.status_code == 200:
        order = response.json()
        products = [
            item
            for item in requests.get(f"{api_url}/carts/{order['cart_id']-1}/items").json()
        ]
        print(products)
        order['products'] = [get_product(flower.get('product_id'),flower.get('quantity')) for flower in products]
        order['address'] = requests.get(f'{api_url}/addresses/{order.get("address_id")}').json()
        return order
    else:
        raise HTTPException(status_code=404, detail="Orders not found")


# update order status by id and status
@app.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: int, order_status: str):
    order = get_order(order_id)
    order['status'] = order_status
    response = requests.put(f"{api_url}/orders/{order_id}", json=order.dict())
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=404, detail="Order not found")


# create order
@app.post("/orders", response_model=Order)
def create_order(order: Order):
    # TODO: To implement
    return order


# delete order by id
@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    # TODO: To implement
    return None
    


# # get cart by id
# @app.get("/carts/{cart_id}", response_model=Cart)
# def get_order(cart_id: int):
#     response = requests.get(f'{api_url}/carts/{cart_id}')
#     if response.status_code == 200:
#         return Cart(**response.json())
#     else:
#         raise HTTPException(status_code=response.status_code, 
#                             detail="Cart not found") 

# # get order by id
# @app.get("/orders/{order_id}", response_model=Order)
# async def get_order(order_id: int):
#     response = requests.get(f'{api_url}/orders/{order_id}')
#     if response.status_code == 200:
#         return Order(**response.json())
#     else:
#         raise HTTPException(status_code=response.status_code,
#                             detail="Order not found") 