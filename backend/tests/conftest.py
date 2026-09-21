"""Fixtures compartidas para las pruebas del detector."""

from __future__ import annotations

import urllib.request
from pathlib import Path

import numpy as np
import pytest

from app.config import SAMPLES_DIR
from app.services.detector import get_model, load_image

BUS_IMAGE_URL = "https://ultralytics.com/images/bus.jpg"
BUS_IMAGE_NAME = "bus.jpg"
DOWNLOAD_HEADERS = {"User-Agent": "IA2-ProyectoFinal/1.0 (academic YOLO tests)"}


def _download_sample(url: str, destination: Path) -> Path:
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    if destination.is_file():
        return destination

    request = urllib.request.Request(url, headers=DOWNLOAD_HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:
        destination.write_bytes(response.read())
    return destination


@pytest.fixture(scope="session")
def yolo_model():
    """Asegura que el modelo se carga una sola vez para toda la sesión de tests."""
    return get_model()


@pytest.fixture(scope="session")
def bus_image(yolo_model) -> np.ndarray:
    image_path = _download_sample(BUS_IMAGE_URL, SAMPLES_DIR / BUS_IMAGE_NAME)
    return load_image(image_path)


@pytest.fixture
def empty_scene() -> np.ndarray:
    """Imagen uniforme: no hay personas ni otros objetos."""
    return np.full((480, 640, 3), 180, dtype=np.uint8)
