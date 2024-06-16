from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from passlib.context import CryptContext
from string import punctuation

app = FastAPI()
base_url = "http://api:8000/users"

# Kontekst do hashowania haseł
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    username: str
    password: str
    is_admin: bool = False


class Login(BaseModel):
    username: str
    password: str

# Endpoint do rejestracji użytkownika


@app.post("/register/")
def register_user(user: User):
    response = requests.get(base_url, params={"username": user.username})
    if response.json():
        # Jeśli lista nie jest pusta, użytkownik już istnieje
        raise HTTPException(status_code=400, detail="Username already exists")
    if len(user.password) < 8 or not any(char in user.password for char in list(punctuation)):
        raise HTTPException(status_code=400, detail="Wrong password format.")

    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    response = requests.post(base_url, json=user.dict())
    return {"message": "User registered successfully."}


# Endpoint do logowania użytkownika
@app.post("/login/")
def login_user(login: Login):
    try:
        response = requests.get(base_url, params={"username": login.username})
        user_data = response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(
            "Invalid access to database"))
    try:

        if len(user_data) > 1:
            raise HTTPException(
                status_code=500, detail="Multiple users with the same username")
        elif len(user_data) == 0:
            raise HTTPException(
                status_code=400, detail="Invalid username or password")

        elif user_data and pwd_context.verify(login.password, user_data[0]['password']):
            return {"message": "Login successful", "is_admin": user_data[0]['is_admin'], "user_id": user_data[0]['id']}
        else:
            raise HTTPException(
                status_code=400, detail="Invalid username or password")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(
            "Something went wrong. Please try again."))
