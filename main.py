from fastapi import FastAPI #importamos fastapi
from routers import products, users, basic_auth_users, jwt_auth_users
from fastapi.staticfiles import StaticFiles
#import FastApi.routers.users as users

app = FastAPI() #intanciamos fastaspi

#Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

#inicializa el servce: uvicorn main:app --reload

@app.get("/") # get Se utiliza para solicitar datos de un servidor. la raiz(/) llama al localhost
async def root():
    return"Hola FastAPI"

@app.get("/url")
async def url():
    return {"url": "https://joyeriafarro.pe/aretes"}