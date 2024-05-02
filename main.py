from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database.db import init_db
from src.routes import (
    event,
    registration
)

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


description = """
    API for managing events and registrations
"""

app = FastAPI(
    lifespan=lifespan,
    title="TICKETEK - Event Management API",
    description=description,
    version="0.0.1",
)

app.include_router(event.event)
app.include_router(registration.registration)