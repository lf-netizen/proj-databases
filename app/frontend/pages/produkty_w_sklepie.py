import streamlit as st
import aiohttp
import asyncio
from pydantic import BaseModel, Field
from nanoid import generate
from front_objects.navigation import make_sidebar
from front_objects.utils import Links
photo_url = "http://api:8000/files/download/"
import requests
from io import BytesIO
from PIL import Image
from typing import List
import nanoid
import datetime


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
    
class SecretCompanyApp:
    def __init__(self):
        make_sidebar()

    def run(self):
        st.write(
            """
        # 🌸 Flower shop
        Feel Free, buy everything you want!
        """
        )

        products = asyncio.run(self.ask_products())
        self.display_product_tiles(products)

    @staticmethod
    async def get_all_products():
        base_url = "http://api:8000"
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_url}/products/") as response:
                products = await response.json()
                return [Product(**product) for product in products if product['is_enabled']]

    @staticmethod
    async def ask_products():
        products = await SecretCompanyApp.get_all_products()
        return products
    
    @staticmethod
    def show_photo(product_photo_id: str):
        response = requests.get(f"{photo_url}{product_photo_id}", stream=True)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            return image
        else:
            return None
    
    @staticmethod
    def filter_products(products, phrase):
        return [product for product in products if product.name.lower().startswith(phrase.lower())]

    @staticmethod
    def display_product_tiles(products):
        phrase = st.text_input("Filter products by name:")
        filter_results = SecretCompanyApp.filter_products(products, phrase)
        
        product_index = 0
        while product_index < len(filter_results):
            col1, col2, col3, col4 = st.columns(4)
            for col in [col1, col2, col3, col4]:
                with col:
                    if product_index < len(filter_results):
                        product = filter_results[product_index]
                        if st.button(product.name, key=product.id):
                            st.session_state.selected_product_id = product.id
                            st.switch_page(Links.PRODUCT_DETAILSC)
                        image = SecretCompanyApp.show_photo(product.image_id)
                        if image:
                            st.image(image, width=100)
                        st.write(f"Price: ${product.sell_price:.2f}")
                        product_index += 1

app = SecretCompanyApp()
app.run()
