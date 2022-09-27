from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from models import init_db
from settings import APP_VERSION


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    init_db(app)


class Greeting(BaseModel):
    message: str


class User(BaseModel):
    username: str


@app.get("/health")
async def healthcheck():
    return {'version': APP_VERSION}


@app.get("/hello/{username}")
async def hello_path(username: str):
    return Greeting(message=f'Hello, {username}!')


@app.get("/hello")
async def hello_query(username: Union[str, None] = None):
    if not username:
        username = 'anonymous'
    return Greeting(message=f'Hello, {username}!')


@app.post("/hello")
async def hello_body(user: User):
    return Greeting(message=f'Hello, {user.username}!')
