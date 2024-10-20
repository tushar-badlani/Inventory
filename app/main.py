from fastapi import FastAPI

from . import models
from .db import engine
from .routers import users, venues, events, permissions

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(venues.router)
app.include_router(events.router)
app.include_router(permissions.router)