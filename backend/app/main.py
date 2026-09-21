"""Aplicación FastAPI: CORS y registro de rutas. La lógica YOLO vive en services/."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import CORS_ORIGINS
from app.services.detector import get_model


@asynccontextmanager
async def lifespan(_app: FastAPI):
    get_model()
    yield


app = FastAPI(
    title="Pedestrian Counter YOLO",
    description="Detecta y cuenta únicamente personas en una imagen.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
