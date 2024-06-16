import streamlit as st
from front_objects.navigation import make_sidebar
from front_objects.utils import Links
import requests
from front_objects.classes.product import Product

base_url = "http://api:8000"

def get_product(product_id: str):
    response = requests.get(f"{base_url}/products/{product_id}")
    return response.json()

def display_product_details():
    product_details = get_product(st.session_state.selected_product_id)
    
    chosen_product = Product(**product_details)
    
    st.title(chosen_product.name)
    
    picture = chosen_product.show_photo()
    if picture:
        st.image(picture)
    
    st.write(f"**Price:** {chosen_product.sell_price}")
    st.write(f"**Description:** {chosen_product.description}")
    st.subheader("Purchase product:")
    if int(chosen_product.quantity) > 0:
        quantity = st.number_input("Select product quantity", min_value=1, value=1, max_value=int(chosen_product.quantity))
    else:
        st.warning("Product not available")
        
    if st.button("Add to cart"):
        user_id = st.session_state.user_id
        check_cart = requests.get(f"{base_url}/users/{user_id}/cart")
        
        if check_cart.status_code == 404:
            create_cart = requests.post(f"{base_url}/users/{user_id}/cart", json={})
            add_product = requests.post(f"{base_url}/users/{user_id}/cart/items", json={"product_id": chosen_product.id, "quantity": quantity})
        else:
            add_product = requests.post(f"{base_url}/users/{user_id}/cart/items", json={"product_id": chosen_product.id, "quantity": quantity})
            if add_product.status_code == 200:
                st.success('Product added')
            else:
                st.error('Something went wrong')
        
    if st.button("Browse reviews"):
        
        all_opinions = requests.get('http://api:8000/opinions/',params={'product_id':st.session_state.selected_product_id}).json()
        if all_opinions:
            st.info("Product reviews:")
            for index,opinion in enumerate(all_opinions):
                st.write(f'{index+1}. {opinion.get("content")}')
        else:
            st.info("No reviews yet!")
    if st.button("Back to all products"):
        del st.session_state.selected_product_id
        st.switch_page(Links.ALL_PRODUCTS)

    st.write(f"**Category:** {chosen_product.tags}")

make_sidebar()
display_product_details()
