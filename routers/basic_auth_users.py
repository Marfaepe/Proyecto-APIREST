from fastapi import FastAPI #importamos fastapi
from pydantic import BaseModel
from fastapi import  APIRouter

app = FastAPI() #intanciamos fastaspi

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str


users_db = {
    "mardev":{
        "username": "mardev",
        "full_name": "Martha Farro",
        "email": "martha@gmail.com",
        "disabled": False,
        "password": "123456"
    },
    "pedrodev":{
        "username": "pedrodev",
        "full_name": "Pedro Ruiz",
        "email": "pedro@gmail.com",
        "disabled": True,
        "password": "654321"
    },
}

def search_user(username: str):
   if username in users_db:
       return UserDB(users_db[username])