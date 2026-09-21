"""Pruebas del conteo de personas. Solo la clase person debe sumar al total."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from app.config import PERSON_CLASS_ID, PERSON_CLASS_NAME
from app.services.detector import detect_people, get_model, load_image

# En COCO: car=2, bus=5, truck=7. Se usan para comprobar que hay vehículos y no se cuentan.
VEHICLE_CLASS_IDS = {2, 5, 7}


def _class_ids(image: np.ndarray, confidence_threshold: float = 0.50) -> list[int]:
    results = get_model().predict(
        source=image,
        conf=confidence_threshold,
        verbose=False,
    )
    if not results or results[0].boxes is None:
        return []
    return [int(box.cls[0]) for box in results[0].boxes]


def test_image_with_people_detects_people(bus_image: np.ndarray) -> None:
    result = detect_people(bus_image)

    assert result.total_people > 0
    assert result.total_people == len(result.detections)
    assert all(detection.class_name == PERSON_CLASS_NAME for detection in result.detections)


def test_image_without_people_counts_zero(empty_scene: np.ndarray) -> None:
    result = detect_people(empty_scene)

    assert result.total_people == 0
    assert result.detections == []


def test_cars_without_people_count_zero(bus_image: np.ndarray) -> None:
    # En bus.jpg las personas aparecen más abajo; este recorte deja el autobús y ninguna persona.
    vehicle_crop = bus_image[:400, :, :]
    raw_ids = _class_ids(vehicle_crop)

    if PERSON_CLASS_ID in raw_ids:
        pytest.skip("El recorte del vehículo todavía incluye una persona.")

    result = detect_people(vehicle_crop)

    assert result.total_people == 0
    assert VEHICLE_CLASS_IDS.intersection(raw_ids), "El recorte debería contener un vehículo."


def test_mixed_scene_counts_only_people(bus_image: np.ndarray) -> None:
    raw_ids = _class_ids(bus_image)
    person_in_raw = raw_ids.count(PERSON_CLASS_ID)
    has_other_objects = any(class_id != PERSON_CLASS_ID for class_id in raw_ids)

    assert person_in_raw > 0
    assert has_other_objects, "La imagen de bus debería incluir otros objetos además de personas."

    result = detect_people(bus_image)

    assert result.total_people == person_in_raw
    assert all(detection.class_name == PERSON_CLASS_NAME for detection in result.detections)
    assert VEHICLE_CLASS_IDS.intersection(raw_ids)


def test_invalid_image_raises(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="vacía o no se pudo leer"):
        detect_people(None)

    with pytest.raises(ValueError, match="vacía o no se pudo leer"):
        detect_people(np.array([]))

    corrupted_file = tmp_path / "corrupta.jpg"
    corrupted_file.write_bytes(b"esto no es una imagen")
    with pytest.raises(ValueError, match="No se pudo leer la imagen"):
        load_image(corrupted_file)


def test_confidence_threshold_filters_detections(bus_image: np.ndarray) -> None:
    # Un umbral más alto reduce falsos positivos, pero puede omitir personas reales.
    low_threshold = detect_people(bus_image, confidence_threshold=0.10)
    high_threshold = detect_people(bus_image, confidence_threshold=0.90)

    assert high_threshold.total_people <= low_threshold.total_people
    assert all(detection.confidence >= 0.90 for detection in high_threshold.detections)
    assert all(detection.confidence >= 0.10 for detection in low_threshold.detections)


def test_original_image_is_not_modified(bus_image: np.ndarray) -> None:
    original = bus_image.copy()

    detect_people(bus_image)

    assert np.array_equal(bus_image, original)
