from front_objects.navigation import make_sidebar
import streamlit as st
import pandas as pd
from front_objects.utils import Links
import requests
from io import BytesIO
from PIL import Image

make_sidebar()
base_url = "http://api:8000"

def change_quantity(item_id, quantity, product_id):
    requests.delete(f"{base_url}/users/{st.session_state.user_id}/cart/items/{item_id}")
    if quantity > 0:
        requests.post(f"{base_url}/users/{st.session_state.user_id}/cart/items", 
                      json={"product_id": product_id, "quantity": quantity})
    st.rerun()

def show_photo(product_photo_id: str):
    response = requests.get(f"http://api:8000/files/download/{product_photo_id}", stream=True)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    else:
        return None

st.write("# 🛒 Shopping Cart")

get_items_in_cart = requests.get(f"{base_url}/users/{st.session_state.user_id}/cart/items").json()

if type(get_items_in_cart) == list and len(get_items_in_cart) > 0:
    all_ids = []
    # Headers for the table
    
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])

    col1.subheader("Product Name")
    col2.subheader("Price per Unit")
    col3.subheader("Quantity")
    col4.subheader("Total")
    col5.subheader("")

    total_cost = 0

    for i in get_items_in_cart:
        item_id = i["id"]
        product_id = str(i["product_id"])
        if product_id not in all_ids:
            all_ids.append(product_id)
        chosen_quantity = i["quantity"]
        
        get_item_details = requests.get(f"{base_url}/products/{product_id}").json()
        item_name = get_item_details["name"]
        item_price = get_item_details["sell_price"]
        actual_quantity = get_item_details["quantity"]
        
        if chosen_quantity > actual_quantity:
            change_quantity(item_id, actual_quantity, product_id)
        
        item_total_cost = item_price * chosen_quantity
        total_cost += item_total_cost
        
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
        
        with col1:
            st.write(f"{item_name}")
        with col2:
            st.write(f"${item_price} /unit")
        with col3:
            new_quantity = st.number_input("", min_value=0, max_value=actual_quantity, value=chosen_quantity, step=1, key=f"quantity_{item_id}")
        with col4:
            st.write(f"${item_total_cost:.2f}")
        with col5:
            if new_quantity != chosen_quantity:
                if st.button("Update", key=f"update_{item_id}"):
                    change_quantity(item_id, new_quantity, product_id)

    st.write(f"**Total Cost:** ${total_cost:.2f}")
    resp = requests.post(f'http://reccomend:8008/freq_together',json=all_ids).json()
    st.write('')
    st.write('*Frequently purchased together*')
    buts=  st.columns(6)
    for col,item in zip(buts,resp):
        with col:
            if st.button(f'{item.get("name")}',key=str(item.get('name'))):
                st.session_state.selected_product_id = item.get("id")
                st.switch_page(Links.PRODUCT_DETAILSC)
            curr_image = show_photo(item.get('image_id'))
            st.image(curr_image, width=90)
            st.write(f"Cena: ${item.get('sell_price')}")
    
    if st.button("Checkout"):
        st.switch_page(Links.SEND_PAGE)


else:
    st.write("Your cart is empty.")
