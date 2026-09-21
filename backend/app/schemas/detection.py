"""Contrato HTTP de detección. Nombres en inglés para compatibilidad con frontend TypeScript."""

from pydantic import BaseModel, Field


class BoundingBoxSchema(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int


class DetectionSchema(BaseModel):
    class_name: str
    confidence: float
    bounding_box: BoundingBoxSchema


class DetectionResponse(BaseModel):
    total_people: int
    detections: list[DetectionSchema]
    image_result: str = Field(description="Annotated image in JPEG, encoded in base64.")


class HealthResponse(BaseModel):
    status: str
