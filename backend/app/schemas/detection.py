"""Contrato HTTP de detección. Internamente el código usa nombres en inglés."""

from pydantic import BaseModel, Field


class BoundingBoxSchema(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int


class DetectionSchema(BaseModel):
    clase: str
    confianza: float
    caja: BoundingBoxSchema


class DetectionResponse(BaseModel):
    total_personas: int
    detecciones: list[DetectionSchema]
    imagen_resultado: str = Field(description="Imagen anotada en JPEG, codificada en base64.")


class HealthResponse(BaseModel):
    status: str
