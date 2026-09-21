"""Rutas HTTP. Validan la entrada y delegan la detección al servicio YOLO."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.config import ALLOWED_EXTENSIONS, ALLOWED_MIME_TYPES, MAX_UPLOAD_BYTES
from app.schemas.detection import (
    BoundingBoxSchema,
    DetectionResponse,
    DetectionSchema,
    HealthResponse,
)
from app.services.detector import (
    detect_people,
    encode_image_as_jpeg_base64,
    load_image_from_bytes,
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/detect", response_model=DetectionResponse)
async def detect(file: UploadFile = File(...)) -> DetectionResponse:
    image_bytes = await file.read()
    _validate_upload(file.filename, file.content_type, len(image_bytes))

    try:
        image = load_image_from_bytes(image_bytes)
        result = detect_people(image)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error

    # Cero personas no es un error: se devuelve total_people = 0.
    return DetectionResponse(
        total_people=result.total_people,
        detections=[
            DetectionSchema(
                class_name=detection.class_name,
                confidence=round(detection.confidence, 4),
                bounding_box=BoundingBoxSchema(
                    x1=detection.x1,
                    y1=detection.y1,
                    x2=detection.x2,
                    y2=detection.y2,
                ),
            )
            for detection in result.detections
        ],
        image_result=encode_image_as_jpeg_base64(result.annotated_image),
    )


def _validate_upload(filename: str | None, content_type: str | None, size: int) -> None:
    if not filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo está vacío o no tiene nombre.",
        )

    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato no permitido. Use JPG, PNG o WEBP.",
        )

    mime_type = (content_type or "").split(";")[0].strip().lower()
    if mime_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de archivo no permitido.",
        )

    if size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo está vacío.",
        )

    if size > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo supera el tamaño máximo permitido.",
        )
