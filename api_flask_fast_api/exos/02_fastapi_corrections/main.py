from fastapi import FastAPI
import uvicorn

from routers.users import router as users_router
from routers.auth import router as auth_router
from routers.products import router as products_router

app = FastAPI(title="Exercice FastAPI",version="1.0.0",description="Validation FASTAPI")

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(products_router)

if __name__ == "__main__":
    uvicorn.run("main:app",host='0.0.0.0',port=8000,reload=True)