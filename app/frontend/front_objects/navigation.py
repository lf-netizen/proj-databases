import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages

from .utils import Links

from .recomend_system import RecomendSystem

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.title("**PLANT SHOP**")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.write(f"Welcome **{st.session_state.username}**")


            st.page_link(f"{Links.MAIN_USER_PAGE}", label="Products", icon="🛍️")
            st.page_link(f"{Links.PAGE_2}", label="Shopping Cart", icon="🛒")
            st.page_link(f"{Links.CHATBOT_PAGE}", label="Chatbot", icon="💬")
            st.page_link(f"{Links.ORDER_HISTORY}", label="Order History", icon="📜")

            st.write("")
            st.write("")
            with st.container():
                if st.button("Log out"):
                            logout()
            
            
            st.write("*Recommendations*")
            
            recomendations = RecomendSystem()
            recomendations.run()
            
        elif get_current_page_name() != "streamlit_app":
            st.switch_page(Links.MAIN_PROGRAM)


def logout():
    st.session_state.logged_in = False
    st.info("Logged out successfully!")
    sleep(0.05)
    st.switch_page(Links.MAIN_PROGRAM)
    