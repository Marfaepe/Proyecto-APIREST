from fastapi import APIRouter, HTTPException
from pydantic import BaseModel #BaseModel da la capacidad de crear una entidad

router = APIRouter() 

#inicializa el servce: uvicorn users:app --reload

#Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id= 1, name="Martha", surname="Farro", url="https://joyeriafarro.pe/",age= 35),
              User(id= 2, name="Susana", surname="Espino", url="https://joyeria.pe/",age= 20),
              User( id = 3, name="Pedro", surname="Arnesto", url="https://farro.pe/", age= 50),
              User(id = 4, name= "Jacinto", surname= "Nesto", url="https://nesto.pe/", age= 25)]
         

@router.get("/usersjson") 
async def usersjson():
    return [{"name": "Martha", "surname": "Farro", "url":"https://joyeriafarro.pe/", "age": 35},
            {"name": "Susana", "surname": "Espino", "url":"https://joyeria.pe/", "age": 20},
            {"name": "Pedro", "surname": "Arnesto", "url":"https://farro.pe/", "age": 50},
            {"name": "Jacinto", "surname": "Nesto", "url":"https://nesto.pe/", "age": 25},
            ]

@router.get("/users")
async def users():
    return users_list


#path
@router.get("/user/{id}")
async def user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}

#query    
@router.get("/user/")
async def user(id: int):
    return search_user(IndexError)
      

@router.post("/user/", response_model= User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
       raise HTTPException(status_code=404, detail="El usuario ya existe")
            
    users_list.append(user)
    return user

@router.put("/user/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if  not found:
        return{"error": "No se ha actualizado el usuario"}     
    else:
        return user
    


#path
@router.delete("/user/{id}")
async def user(id: int):

    found = False
    for index, save_u in enumerate(users_list):
        if save_u.id == id:
            del users_list[index]
            found = True
    if not found:
            return{"error": "No se ha eliminado el usuario"}  
        

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}     