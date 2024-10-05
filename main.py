from fastapi import FastAPI #importamos fastapi
from routers import products, users
#import FastApi.routers.users as users

app = FastAPI() #intanciamos fastaspi

#Routers
app.include_router(products.router)
app.include_router(users.router)

#inicializa el servce: uvicorn main:app --reload

@app.get("/") # get Se utiliza para solicitar datos de un servidor. la raiz(/) llama al localhost
async def root():
    return"Hola FastAPI"

@app.get("/url")
async def url():
    return {"url": "https://joyeriafarro.pe/aretes"}