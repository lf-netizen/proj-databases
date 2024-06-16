import streamlit as st
import requests
from front_objects.navigation import make_sidebar
from front_objects.utils import Links
from front_objects.classes.order import OrderStatus

make_sidebar()

def get_order_history(user_id):
    try:
        response = requests.get(f"http://history_orders:8007/orders/{user_id}")
        response.raise_for_status()
        orders = response.json()
        return orders
    except requests.exceptions.HTTPError as err:
        st.error(f"HTTP error occurred: {err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")

def display_order_details(order):
    st.markdown(f"### Order Details for ID #{order['id']}")
    st.markdown(f"**Order Status:** {order['status']}")
    st.markdown(f"**Total Amount:** ${round(order['total_amount'],2)}")
    st.markdown(f"**Order Date:** {order['date']}")

    st.markdown("#### Products:")
    for product in order['products']:
        st.markdown(f"""
        <div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px;">
            <strong>Product:</strong> {product['name']}<br>
            <strong>Price:</strong> ${product['sell_price']}<br>
            <strong>Quantity:</strong> {product['quantity']}<br>
            
        </div>
        """, unsafe_allow_html=True)

        if (order['status'] == "DELIVERED" or order['status'] == "RETURNED") and not product.get('review'):
            st.write(f"Add review for {product['name']}")
            review_text = st.text_area(
                "Your review", key=f"review_text_{order['id']}_{product['name']}")
            if st.button("Submit Review", key=f"submit_button_{order['id']}_{product['name']}"):
                send_review(
                    st.session_state.user_id, order['id'], product['id'], review_text,product['name'])

def send_review(user_id, order_id, product_id, review,name):
    review_data = {
        "user_id": user_id,
        "order_id": order_id,
        "product_id": product_id,
        "content": review
    }
    try:
        response = requests.post(
            "http://history_orders:8007/review", json=review_data)
        response.raise_for_status()
        st.success(f"Review for {name} has been successfully submitted!")
    except requests.exceptions.HTTPError as err:
        st.error(f"HTTP error occurred: {err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")

st.title("Your Order History")

username = st.session_state.get("username", None)

if username:
    orders = get_order_history(st.session_state.user_id)
    if orders:
        orders.reverse()
        for order in orders[:20]:
            with st.expander(f"Order #{order['id']}"):
                display_order_details(order)
    else:
        st.write("No orders found!")
else:
    st.write("Please log in to view your order history.")
