import streamlit as st
import requests
from pydantic import BaseModel, Field
import nanoid

from front_objects.navigation_admin import make_sidebar
make_sidebar()
from PIL import Image
from io import BytesIO
from front_objects.classes.product import Product

def show_photo(product_photo_id: str):
    photo_url_dowland = "http://api:8000/files/download/"
    response = requests.get(f"{photo_url_dowland}{product_photo_id}", stream=True)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    else:
        return None

def delete_product(selected_product: Product):
    selected_product.is_enabled = False
    response = requests.put(f"{api_url}/products/{selected_product.id}", json=selected_product.dict())


api_url = "http://api:8000"
photo_url = "http://api:8000/files/upload"

st.title("Shop Management System")

# Fetch product list
response = requests.get(f"{api_url}/products")
products = response.json()

joined_list = {product["name"]: product["id"] for product in products if product["is_enabled"]}


selected_product_name = st.selectbox("Choosen product", joined_list, index=None, placeholder="Select a product to edit")


if selected_product_name is not None:
    selected_product_id = joined_list[selected_product_name]
    if selected_product_id:
        response = requests.get(f"{api_url}/products/{selected_product_id}")
        selected_product = Product(**response.json())

        st.write("### Delete Product")
        with st.expander("Delete Product"):
            st.write(f"Are you sure you want to delete this product?")
            if st.button(f"Yes, delete {selected_product_name}"):
                delete_product(selected_product)
            if st.button("No"):
                st.rerun()

        

        st.write("### Edit Product")

        name = st.text_input("Name", selected_product.name)
        description = st.text_area("Description", selected_product.description)
        sell_price = st.number_input("Sell price", value=selected_product.sell_price)
        quantity = st.number_input("Quantity", value=selected_product.quantity)
        buy_price = st.number_input("Buy price", value=selected_product.buy_price)
        tags = st.multiselect("Categories", ["Flower", "flower", "Tree", "Object", "Other", "Manure"], selected_product.tags)
        image_show = show_photo(selected_product.image_id)
        if image_show:
            st.image(image_show)
        image = st.file_uploader("Image", type=['jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG'])

        if st.button("Update Product"):
            updated_product = Product(
                name=name,
                description=description,
                sell_price=sell_price,
                quantity=quantity,
                buy_price=buy_price,
                tags=tags
            )

            # check for name duplicates
            name_check = True
            if selected_product.name != updated_product.name:
                response = requests.get(f'{api_url}/products/name/{updated_product.name}')
                if response.status_code == 200:
                    name_check = False
                    st.error('This product name is already occupied!')
            
            if name_check:
                if image is None:
                    updated_product.image_id = selected_product.image_id
                else:
                    updated_product.add_product_image(image)
                    
                response = requests.put(f"{api_url}/products/{selected_product_id}", json=updated_product.dict())
                
                if response.status_code == 200:
                    st.success("Product updated successfully")
                else:
                    st.error("Failed to update product")
