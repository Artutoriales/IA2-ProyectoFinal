"""Prueba mínima de Fase 1: cargar imagen, detectar personas y mostrar el conteo."""

from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path

import cv2

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.config import OUTPUT_DIR, SAMPLES_DIR
from app.services.detector import detect_people, load_image

SAMPLE_IMAGE_URL = "https://ultralytics.com/images/bus.jpg"
SAMPLE_IMAGE_NAME = "bus.jpg"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detecta y cuenta solo personas en una imagen con YOLO."
    )
    parser.add_argument(
        "image",
        nargs="?",
        help="Ruta a una imagen JPG, PNG o WEBP. Si se omite, se usa una imagen de ejemplo.",
    )
    return parser.parse_args()


def resolve_image_path(image_argument: str | None) -> Path:
    if image_argument:
        image_path = Path(image_argument).expanduser().resolve()
        if not image_path.is_file():
            raise FileNotFoundError(f"No se encontró la imagen: {image_path}")
        return image_path

    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    sample_path = SAMPLES_DIR / SAMPLE_IMAGE_NAME
    if not sample_path.is_file():
        print(f"Descargando imagen de ejemplo: {SAMPLE_IMAGE_URL}")
        urllib.request.urlretrieve(SAMPLE_IMAGE_URL, sample_path)
    return sample_path


def main() -> int:
    args = parse_args()
    image_path = resolve_image_path(args.image)
    image = load_image(image_path)

    result = detect_people(image)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{image_path.stem}_personas.jpg"
    cv2.imwrite(str(output_path), result.annotated_image)

    print(f"Imagen: {image_path}")
    print(f"Personas detectadas: {result.total_people}")
    if result.total_people == 0:
        print("No se detectaron personas.")
    else:
        for index, detection in enumerate(result.detections, start=1):
            print(
                f"  {index}. {detection.class_name} "
                f"{detection.confidence:.0%} "
                f"caja=({detection.x1}, {detection.y1}, {detection.x2}, {detection.y2})"
            )
    print(f"Resultado anotado: {output_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
