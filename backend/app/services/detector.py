"""Detección y conteo de personas con YOLO preentrenado."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from ultralytics import YOLO

from app.config import (
    CONFIDENCE_THRESHOLD,
    MODEL_PATH,
    PERSON_CLASS_ID,
    PERSON_CLASS_NAME,
)

_model: YOLO | None = None


@dataclass(frozen=True)
class PersonDetection:
    class_name: str
    confidence: float
    x1: int
    y1: int
    x2: int
    y2: int


@dataclass(frozen=True)
class DetectionResult:
    total_people: int
    detections: list[PersonDetection]
    annotated_image: np.ndarray


def get_model() -> YOLO:
    """Carga el modelo una sola vez. Se descarga solo si no existe en models/."""
    global _model
    if _model is None:
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        _model = YOLO(str(MODEL_PATH))
    return _model


def load_image(image_path: str | Path) -> np.ndarray:
    """Lee una imagen con OpenCV. No modifica el archivo original."""
    path = Path(image_path)
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(
            f"No se pudo leer la imagen (archivo dañado o formato no válido): {path}"
        )
    return image


def load_image_from_bytes(image_bytes: bytes) -> np.ndarray:
    """Decodifica una imagen en memoria. No guarda el archivo subido en disco."""
    if not image_bytes:
        raise ValueError("La imagen está vacía o no se pudo leer.")

    buffer = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("No se pudo leer la imagen (archivo dañado o formato no válido).")
    return image


def encode_image_as_jpeg_base64(image: np.ndarray) -> str:
    success, encoded = cv2.imencode(".jpg", image)
    if not success:
        raise ValueError("No se pudo generar la imagen de resultado.")
    return base64.b64encode(encoded.tobytes()).decode("ascii")


def detect_people(image: np.ndarray, confidence_threshold: float | None = None) -> DetectionResult:
    """Ejecuta YOLO y conserva únicamente detecciones de la clase person."""
    if image is None or image.size == 0:
        raise ValueError("La imagen está vacía o no se pudo leer.")

    threshold = CONFIDENCE_THRESHOLD if confidence_threshold is None else confidence_threshold
    results = get_model().predict(
        source=image,
        conf=threshold,
        classes=[PERSON_CLASS_ID],
        verbose=False,
    )

    detections: list[PersonDetection] = []
    annotated = image.copy()

    if results:
        boxes = results[0].boxes
        if boxes is not None:
            for box in boxes:
                class_id = int(box.cls[0])
                if class_id != PERSON_CLASS_ID:
                    continue

                confidence = float(box.conf[0])
                x1, y1, x2, y2 = (int(value) for value in box.xyxy[0].tolist())
                detections.append(
                    PersonDetection(
                        class_name=PERSON_CLASS_NAME,
                        confidence=confidence,
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2,
                    )
                )
                _draw_person_box(annotated, x1, y1, x2, y2, confidence)

    return DetectionResult(
        total_people=len(detections),
        detections=detections,
        annotated_image=annotated,
    )


def _draw_person_box(
    image: np.ndarray,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    confidence: float,
) -> None:
    label = f"Person {confidence:.0%}"
    color = (0, 200, 0)
    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size, baseline = cv2.getTextSize(label, font, 0.6, 2)
    text_x2 = x1 + text_size[0] + 6
    text_y1 = max(0, y1 - text_size[1] - baseline - 6)
    cv2.rectangle(image, (x1, text_y1), (text_x2, y1), color, -1)
    cv2.putText(image, label, (x1 + 3, y1 - 6), font, 0.6, (0, 0, 0), 2)
