from fastapi import FastAPI
from app.views import router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router, tags=["rozklady"])
