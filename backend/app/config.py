"""Configuración central del detector.

El umbral de confianza no debe repetirse en el algoritmo: subir CONFIDENCE_THRESHOLD
reduce falsos positivos, pero puede dejar de detectar personas reales.
"""

from __future__ import annotations

import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = BACKEND_DIR / "models"
OUTPUT_DIR = BACKEND_DIR / "output"
SAMPLES_DIR = BACKEND_DIR / "data" / "samples"


def _load_env_file() -> None:
    env_path = BACKEND_DIR / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


_load_env_file()

# En COCO, la clase person tiene id 0. Solo se cuenta esta clase.
PERSON_CLASS_ID = 0
PERSON_CLASS_NAME = "person"

CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.50"))
MODEL_NAME = os.getenv("MODEL_NAME", "yolov8n.pt")
MODEL_PATH = MODELS_DIR / MODEL_NAME

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
MAX_UPLOAD_BYTES = int(float(os.getenv("MAX_UPLOAD_MB", "10")) * 1024 * 1024)
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]
