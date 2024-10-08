from fastapi import FastAPI, Depends, HTTPException, status #importamos fastapi
from pydantic import BaseModel #es una clase de la librería Pydantic que se usa para definir, validar y serializar modelos de datos en Python.
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm #Para la autenticacación usuario y contraseña


app = FastAPI() #intanciamos fastaspi
oauth2 = OAuth2PasswordBearer(tokenUrl = "login")

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


def search_user_db(username: str):
   if username in users_db:
       return UserDB(**users_db[username])


def search_user(username: str):
   if username in users_db:
       return User(**users_db[username])


#Criterio de dependecia
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if  not user:
        raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED, 
             detail="Credenciales de autenticaciónn inválidas", 
             headers={"WWW-Authenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST, 
             detail="Usuario inactivo")

    return user
    

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
         raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED, detail="La contraseña no es correcta")
    
    return {"access_token": user.username , "toke_type": "bearer"}

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
