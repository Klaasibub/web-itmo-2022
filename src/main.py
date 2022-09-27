from fastapi import FastAPI

from api.v1 import auth
from models import init_db
from settings import APP_VERSION


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    init_db(app)


@app.get("/health")
async def healthcheck():
    return {'version': APP_VERSION}


app.include_router(auth.router)
