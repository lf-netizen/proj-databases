import streamlit as st
import requests
from front_objects.navigation_admin import make_sidebar
from front_objects.classes.product import Product

make_sidebar()
api_url = "http://magazyn_stan:8005"

# returns products with quantity up to threshold
def get_low_stock_products(threshold: int = 50):
    response = requests.get(f"{api_url}/products/low_stock/{threshold}")
    return [Product(**product) for product in response.json()]

# restock product given their id and additional stock
def restock_product(product_id: str, additional_stock: int = 5):
    response = requests.post(f"{api_url}/products/restock/{product_id}", json={'additional_stock': additional_stock})
    return response


st.title("Product Management")

stock_threshold = st.number_input(f"Enter stock threshold", min_value=1, max_value=1000)

low_stock_products = get_low_stock_products(stock_threshold)
# st.write(low_stock_products)

if low_stock_products:
    st.header("Products with Low Stock")
    for product in low_stock_products:
        st.subheader(f"Product name: {product.name}")
        # st.write(f"Price: {product.buy_price}")
        st.write(f"Current Stock: {product.quantity}")
        additional_stock = st.number_input(f"Order additional stock for {product.name}", min_value=1, max_value=100, key=product.id)
        if st.button(f"Order for {product.name}", key=f"order_{product.id}"):
            updated_product = restock_product(product.id, additional_stock)
            st.write(updated_product.text)
            st.success(f"Ordered additional {additional_stock} units for {product.name}. New stock: ")
            st.experimental_rerun()
else:
    st.write("No products with low stock.")
