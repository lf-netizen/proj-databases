import streamlit as st
import pandas as pd
import re
import requests
from front_objects.navigation import make_sidebar
from pydantic import BaseModel
from front_objects.utils import Links
from front_objects.classes.product import Product

make_sidebar()

st.write(
    """
## 🛒 SHIPPING DETAILS

Please fill in the details below so we can deliver your order to the specified address.
"""
)

base_url = "http://api:8000"
# Function to validate email
class CartItem(BaseModel):
    product_id: str
    quantity: int

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)


# User data form
with st.form("shipping_form"):
    st.header("Your Shipping Details:")
    first_name = st.text_input("First Name:")
    last_name = st.text_input("Last Name:")
    address = st.text_input("Address:")
    city = st.text_input("City:")
    postal_code = st.text_input("Postal Code:")
    email = st.text_input("Email:")

    payment_method = st.selectbox("Choose payment method:", [
                                  "Credit Card", "Bank Transfer", "PayPal"])

    submitted = st.form_submit_button("Submit Order")
    cart_id = requests.get(f'http://api:8000/users/{st.session_state.user_id}/cart').json()
    items = requests.get(f'http://api:8000/carts/{cart_id.get("id")}/items').json()
    all_ids = [ids.get('product_id') for ids in items]
if submitted:
    
    
    if not all([first_name, last_name, address, city, postal_code, email]) or not validate_email(email):
        st.warning("Please fill in all fields in the form correctly.")
    else:
        get_items_in_cart = requests.get(f"{base_url}/users/{st.session_state.user_id}/cart/items").json()
        total_amount = 0
        for i in get_items_in_cart:
            product_id = i["product_id"]
            qunanity_in_cart = i["quantity"]
            
            product_details_in_shop = requests.get(f"{base_url}/products/{product_id}").json()
            
            product_details_in_shop_obj = Product(**product_details_in_shop)
            
            changed_quantity_product_obj = Product(**product_details_in_shop)
            price_item =  product_details_in_shop_obj.sell_price
            total_amount += price_item*qunanity_in_cart
            quanitity_in_shop = product_details_in_shop_obj.quantity
            
            if quanitity_in_shop > 0 and quanitity_in_shop >= qunanity_in_cart:
                update_quantity = quanitity_in_shop - qunanity_in_cart
                changed_quantity_product_obj.quantity = update_quantity
                
                response = requests.put(f"{base_url}/products/{product_id}", json=changed_quantity_product_obj.dict())          

                
            else: 
                st.switch_page(Links.PAGE_2)
        order_data = {
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "city": city,
            "postal_code": postal_code,
            "email": email,
            "payment_method": payment_method,
            "user_id": st.session_state.user_id,
            "total_amount": total_amount
        }
        

        
        response = requests.post(
            "http://send_order:8006/submit_order/", json=order_data)
        requests.put('http://reccomend:8008/update_orders',json=all_ids)

        if response.status_code == 200:
            st.success("Thank you for your order!")
            st.subheader("Order Summary:")
            st.write(f"First Name: {first_name}")
            st.write(f"Last Name: {last_name}")
            st.write(f"Address: {address}")
            st.write(f"City: {city}")
            st.write(f"Postal Code: {postal_code}")
            st.write(f"Email: {email}")
            st.write(f"Chosen Payment Method: {payment_method}")
            
            
            
            
        else:
            st.write(response)
            st.error("There was an error placing your order. Please try again.")
