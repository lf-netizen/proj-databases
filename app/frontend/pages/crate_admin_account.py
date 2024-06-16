import streamlit as st

from front_objects.navigation_admin import make_sidebar
from front_objects.utils import Links

import requests


make_sidebar()

API_BASE_URL = Links.BACKEND_BASE_URL

def register_user(username, password):
    response = requests.post(f"{API_BASE_URL}/register/", 
                             json={"username": username, "password": password, "is_admin": True})
    return response.json()


st.write("Register a new ADMIN account, the password has to be logner than 8 characters and has one on more specific charakter")
new_username = st.text_input("Choose a username", 
                                key="register_username")
new_password = st.text_input("Choose a password", 
                                type="password", key="register_password")

confirm_password = st.text_input("Confirm password", 
                                    type="password", key="confirm_password")


if st.button("Register"):
    
    if new_password != confirm_password:
        st.error("Passwords do not match. Please try again.")
    else:
        if new_username and new_password:
            response = register_user(new_username, new_password)
        
        if response.get('message') == 'User registered successfully.':
            st.success("Registered successfully! Please log in.")
            
        elif response.get('detail') == 'Username already exists':
            st.error("This username is already in use.")
        else:
            st.error("Password must be at least 8 characters long and include a special character like '#', '@', or '$'.")
