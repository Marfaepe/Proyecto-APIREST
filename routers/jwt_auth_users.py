from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKE_DURATION = 1
SECRET = "bvas67/defgsdNP87957869Idfgsdfgsdfgsd3498J3fgdsgfs91dffg"

router = APIRouter() #intanciamos fastaspi
oauth2 = OAuth2PasswordBearer(tokenUrl = "login")
crypt = CryptContext(schemes= ["bcrypt"])

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


async def auth_user(token: str = Depends(oauth2)):

    exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Credenciales de autenticaciónn inválidas", 
        headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms= [ALGORITHM]).get("sub")
        if username is None:
            raise exception
      
    except JWTError:
            raise exception
    
    return search_user(username)


#Criterio de dependecia
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST, 
             detail="Usuario inactivo")

    return user
    

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
         raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_user_db(form.username)
  
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED, detail="La contraseña no es correcta")
    
    access_token =  {"sub": user.username, 
                     "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKE_DURATION)}
    
    return {"access_token": jwt.encode(access_token, algorithm=ALGORITHM), "toke_type": "bearer"}



@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

