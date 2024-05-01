from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.config.db import init_db
from src.routes import (
    user,
    service,
    token,
)

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


description = """
    Proyecto para Aseguramiento de Calidad
"""

app = FastAPI(
    lifespan=lifespan,
    title="Ticketek API",
    description=description,
    version="0.0.1",
)

app.include_router(user.user)
app.include_router(service.service)
app.include_router(token.token)
