from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import pandas as pd
import os
import requests
import nanoid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from io import BytesIO
from PIL import Image
import numpy as np

image_download_url = "http://api:8000/files/download/"
image_upload_url = "http://api:8000/files/upload"

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

class Product(BaseModel):
    id: str = Field(default_factory=lambda: nanoid.generate(size=10))
    name: str
    description: str = "default description"
    sell_price: float = 0
    quantity: int = 0
    buy_price: float = 0
    date: str = Field(default_factory=lambda: datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    image_id: str | None = None
    tags: List[str] = Field(default_factory=list)
    is_enabled: bool = True
    
    def show_photo(self):
        response = requests.get(f"{image_download_url}{self.image_id}", stream=True)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            return image
        else:
            return None

    # Function to compress image
    @staticmethod
    def compress_image(img: Image.Image, output_size=(320, 320), quality=70) -> BytesIO:
        img.thumbnail(output_size)
        output = BytesIO()
        img.save(output, format='PNG', quality=quality)
        output.seek(0)
        return output

    # Function to add product image
    def add_product_image(self, file):
        img = self.compress_image(Image.open(file))
        img_extension = file.split('.')[-1]
        files = {'file': (f'{self.date}_{self.name}.{img_extension}', img, f'image/{img_extension}')}
        response = requests.post(image_upload_url, files=files)
        response.raise_for_status()  # Check for request errors
        self.image_id = response.json().get('file_id')
        return response

def create_user(username, password, is_admin=False):
    user_data = {
        "username": username,
        "password": password,
        "is_admin": is_admin,
    }
    resp = requests.get("http://api:8000/users/").json()
    all_users = [user.get('username') for user in resp]
    if username not in all_users:
        response = requests.post("http://api:8000/users/", json=user_data)
        return response.json()
    else:
        print("user with this name exists")

def init_qdrant(data, qdrant_url: str):
    vec_len = 384 #lenght of vector for embedding model
    client = QdrantClient(url=qdrant_url)
    names = [item.name for item in client.get_collections().collections]
    
    if 'products_description' not in names:
        client.create_collection(
            collection_name="products_description",
            vectors_config=VectorParams(size=vec_len, distance=Distance.COSINE),
        )
    else:
        print('Collection exists')

def add_order(adres:Address, user_id:int, items: Dict, base_url:str):
    create_cart = requests.post(f"http://{base_url}/users/{user_id}/cart", json={})

    for flower,quantity in items.items():
        add_product = requests.post(f"http://{base_url}/users/{user_id}/cart/items", json={"product_id": flower, "quantity": quantity})

    response = requests.post(f"http://{base_url}/addresses",
                                json=adres.model_dump()).json()
    address_id = response.get('id')

    response = requests.post(f"http://{base_url}/users/{user_id}").json()
    cart_id = create_cart.json().get('id')

    items = requests.get(
        f"http://{base_url}/carts/{cart_id}/items").json()
    products = [
        requests.get(f"http://{base_url}/products/{item['product_id']}").json()
        for item in items
    ]
    total_amount = round(sum(item['quantity'] * product['sell_price']
                       for item, product in zip(items, products)),2)
    dborder = OrderDb(
        status="DELIVERED",
        total_amount=total_amount,
        address_id=address_id,
        user_id=user_id,
        cart_id=cart_id,
    )
    print(dborder.model_dump())
    response = requests.post(f"http://{base_url}/orders",
                             json=dborder.model_dump())
    



def main():
    data_path = 'init_data/products/flowershopdata_clean.csv'
    data = pd.read_csv(data_path)

    qdrant_url = "http://qdrant:6333"
    init_qdrant(data, qdrant_url)
    
    for _,item in data.iterrows():
        product = Product(
        id =  item['id'],
        name= item['Name'][0] + item['Name'][1:].lower(),
        description= item['Description'],
        sell_price= item['Sale_price'],
        quantity= item['Quantities'],
        buy_price= item['Buy_price'],
        date= 'None',
        tags= [item['tags']],
        is_enabled= True
        )
        response = requests.get(f'http://api:8000/products/name/{product.name}')
        if response.status_code == 200:
            print('Product exists')
        else:
            product.add_product_image(item['pic_path'])
            response = requests.post(f'http://api:8000/products/', json=product.dict())
            if response.status_code == 200:
                print('Product created')

    
    create_user('TestA','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',1)
    create_user('TestU','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',0)
    create_user('User1','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',0)
    create_user('User2','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',0)
    create_user('User3','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',0)
    create_user('User4','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',0)
    create_user('User5','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',0)
    create_user('User6','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',0)
    create_user('User7','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',0)
    create_user('User8','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',0)
    create_user('User9','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',0)
    create_user('User10','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',0)
    create_user('User11','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',0)
    create_user('User12','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',0)
    create_user('User13','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',0)
    create_user('User14','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',0)
    create_user('User15','$2b$12$kj2seUugJ5DLVV8YoPSUyuChpTdQYxBIIGt.rYtJZZIekcQUxHfaG',0)

    addresses = pd.read_csv('init_data/addresses.csv')
    df_orders = pd.read_csv('init_data/orders.csv')
    for order in df_orders.iterrows():
        order_dict = {order[1].values[1] : order[1].values[6],
                    order[1].values[2] : order[1].values[7],
                    order[1].values[3] : order[1].values[8],
                    order[1].values[4] : order[1].values[9],
                    order[1].values[5] : order[1].values[10]}
        user_id = np.random.randint(low=1,high=17)
        adres = Address(**addresses.iloc[user_id].to_dict())
        add_order(adres,user_id,order_dict,'api:8000')
    requests.post('http://api:8000/opinions/',json={'user_id':4, "product_id": "_ihvY2cxEF","content": "Beautiful"})
    requests.post('http://api:8000/opinions/',json={'user_id':5, "product_id": "X8tcuAiPKf","content": "Very pretty"})
    requests.post('http://api:8000/opinions/',json={'user_id':6, "product_id": "sF4-20cYQc","content": "A bit pricy"})
    requests.post('http://api:8000/opinions/',json={'user_id':4, "product_id": "_ihvY2cxEF","content": "I like it a lot"})
    requests.post('http://api:8000/opinions/',json={'user_id':6, "product_id": "sF4-20cYQc","content": "Looks beautiful in my garden"})

if __name__ == "__main__":
    main()
