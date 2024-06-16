import requests
import streamlit as st
from .utils import Links
import random
from io import BytesIO
from PIL import Image


class RecomendSystem:
    def __init__(self) -> None:
        self.formated_products = []
        self.photo_url = "http://api:8000/files/download/"
        
    def get_products(self,N):
        products = requests.get(f'http://reccomend:8008/get_reccomendations/{N}').json()
        for product in products:
            cena = "${:.2f}".format(product.get('sell_price')) 
            formated = {"name": product.get('name'), "image": product.get('image_id'), "price": cena,"id": product.get('id')}
            self.formated_products.append(formated)

    def __show_photo__(self,product_photo_id: str):
        response = requests.get(f"{self.photo_url}{product_photo_id}", stream=True)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            return image
        else:
            return None
        
    def display(self):
        index = 0
        while index < len(self.formated_products):
            col1, col2, col3 = st.columns([50,50,50])
            for col in [col1, col2, col3]:
                with col:
                    if index < len(self.formated_products):
                        current = self.formated_products[index]
                        if st.button(f'{current.get("name")}'):
                            st.session_state.selected_product_id = current.get("id")
                            st.switch_page(Links.PRODUCT_DETAILSC)
                        curr_image = self.__show_photo__(current.get('image'))
                        st.image(curr_image, width=60)
                        st.write(f"Cena: {current.get('price')}")
                        index += 1
                        
    def run(self):
        self.get_products(N=3)
        self.display()
        
        if st.button("Refresh"):
            self.formated_products.clear()
