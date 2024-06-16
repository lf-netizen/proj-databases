# Run the backend 
cd backend/login_register

uvicorn fast:app --reload --port 5000

# Run the frontend

cd streamlit_front

streamlit run streamlit run streamlit_app.py

Do not run streamlit from higher dictionary, becouse of the pages wont run correctly.