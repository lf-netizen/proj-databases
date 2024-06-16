import nanoid
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from pathlib import Path
from fastapi import UploadFile
from PIL import Image
from io import BytesIO
import requests

image_upload_url = "http://api:8000/files/upload"
image_download_url = "http://api:8000/files/download/"

class Product(BaseModel):
    id: str = Field(default_factory=lambda: nanoid.generate(size=10))
    name: str = ''
    description: str = ''
    sell_price: float = 0
    quantity: int = 0
    buy_price: float = 0
    date: str = Field(default_factory=lambda: datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    image_id: str | None = None
    tags: List[str] = Field(default_factory=list)
    is_enabled: bool = True

class VecProduct(BaseModel):
    id: str = ''
    name: str = ''
    description: str = ''
    is_enabled: bool = True
   
def add_product_image(file: UploadFile, product: Product):
    img = compress_image(Image.open(file.file))
    img_extension = file.filename.split('.')[-1]
    file = {'file': (f'{product.date}_{product.name}.{img_extension}', img, f'image/{img_extension}')}
    response = requests.post(image_upload_url, files=file)
    product.image_id = response.json()['file_id']
    return response
    
def compress_image(img: Image.Image, output_size=(320, 320), quality=70) -> BytesIO:
    img.thumbnail(output_size)
    output = BytesIO()
    img.save(output, format='png', quality=quality)
    return output.seek(0)

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str = "default description"
    sell_price: float = 0
    quantity: int = 0
    buy_price: float = 0
    date: str | None = None
    image_id: str | None = None
    tags: List[str] = Field(default_factory=list)


# import nanoid
# from typing import List
# from pydantic import BaseModel, Field


# class Product(BaseModel):
#     id: str = Field(default_factory=lambda: nanoid.generate(size=10))
#     name: str
#     price: float
#     quantity: int = 0
#     description: str = ""
#     category: str
#     tags: List[str] = []


# class ProductUpdate(BaseModel):
#     name: str | None = None
#     price: float | None = None
#     quantity: int | None = None
#     description: str | None = None
#     category: str | None = None
#     tags: List[str] | None = None