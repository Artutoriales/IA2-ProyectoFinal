"""Pruebas de los endpoints HTTP. No cubren webcam ni frontend."""

from __future__ import annotations

import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_detect_counts_people_in_bus_image(client: TestClient, bus_image: np.ndarray) -> None:
    image_bytes = _encode_jpeg(bus_image)

    response = client.post(
        "/detect",
        files={"file": ("bus.jpg", image_bytes, "image/jpeg")},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["total_personas"] > 0
    assert payload["total_personas"] == len(payload["detecciones"])
    assert all(item["clase"] == "person" for item in payload["detecciones"])
    assert payload["imagen_resultado"]


def test_detect_zero_people_is_not_an_error(client: TestClient, empty_scene: np.ndarray) -> None:
    image_bytes = _encode_jpeg(empty_scene)

    response = client.post(
        "/detect",
        files={"file": ("vacio.jpg", image_bytes, "image/jpeg")},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["total_personas"] == 0
    assert payload["detecciones"] == []


def test_detect_rejects_empty_file(client: TestClient) -> None:
    response = client.post(
        "/detect",
        files={"file": ("vacio.jpg", b"", "image/jpeg")},
    )

    assert response.status_code == 400


def test_detect_rejects_invalid_extension(client: TestClient) -> None:
    response = client.post(
        "/detect",
        files={"file": ("modelo.pt", b"not-an-image", "application/octet-stream")},
    )

    assert response.status_code == 400
    assert "Formato no permitido" in response.json()["detail"]


def test_detect_rejects_corrupted_image(client: TestClient) -> None:
    response = client.post(
        "/detect",
        files={"file": ("corrupta.jpg", b"esto no es una imagen", "image/jpeg")},
    )

    assert response.status_code == 400


def test_detect_rejects_oversized_file(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.api.routes.MAX_UPLOAD_BYTES", 16)

    response = client.post(
        "/detect",
        files={"file": ("grande.jpg", b"x" * 32, "image/jpeg")},
    )

    assert response.status_code == 400
    assert "tamaño máximo" in response.json()["detail"]


def _encode_jpeg(image: np.ndarray) -> bytes:
    success, encoded = cv2.imencode(".jpg", image)
    assert success
    return encoded.tobytes()
