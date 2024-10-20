from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from . import models
from .db import engine
from .routers import users, venues, events, permissions

origins = ["*"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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