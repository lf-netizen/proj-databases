from front_objects.navigation import make_sidebar
import streamlit as st
import requests
make_sidebar()
import streamlit as st
from front_objects.utils import Links

st.title("ChatBot 💬")
st.write("Feel free to ask me anything! I'm here to help.")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"
def get_stream(question):
    s = requests.Session()
    with s.get(f'http://chatbot:8009/ask/{question}', timeout=5, stream=True) as resp:
        for chunk in resp:
            st.session_state.product_id = chunk
            st.session_state.product_name = chunk
            yield chunk.decode()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for index,message in enumerate(st.session_state.messages):
    if message["role"] == 'user' or message['role'] == 'Assistant':
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get('id'):
                if st.button(message["name"],key=index):
                    st.session_state.selected_product_id = message["id"]
                    st.switch_page(Links.PRODUCT_DETAILSC)
            

# Accept user input
if question := st.chat_input(""):
    info = ''
    name = ''
    id = ''
    all_flowers = requests.get(f'http://chatbot:8009/ask/names/{question}').json()
    with st.chat_message("User"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("Assistant"):
        response =st.write_stream(get_stream(question))
        for flower in all_flowers:
            if flower in response:
                info = requests.get(f'http://api:8000/products/name/{flower}').json()
                id =  info.get('id')
                name = info.get('name')
    st.session_state.messages.append({"role": "Assistant", "content": response,
                                      "name":name, "id":id})

    st.rerun()

        

    