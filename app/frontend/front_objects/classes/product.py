import nanoid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
import requests
from io import BytesIO
from PIL import Image
from typing import Optional


image_download_url = "http://api:8000/files/download/"
image_upload_url = "http://api:8000/files/upload"


class Product(BaseModel):
    id: str = Field(default_factory=lambda: nanoid.generate(size=10))
    name: str
    description: str = "default description"
    sell_price: float = 0
    quantity: int = 0
    buy_price: float = 0
    date: str = Field(default_factory=lambda: datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    image_id: Optional[str] = None
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
        img_extension = file.name.split('.')[-1]
        files = {'file': (f'{self.date}_{self.name}.{img_extension}', img, f'image/{img_extension}')}
        response = requests.post(image_upload_url, files=files)
        response.raise_for_status()  # Check for request errors
        self.image_id = response.json().get('file_id')
        return response