# Backend - Pedestrian Counter YOLO

Backend Python/FastAPI para el sistema de detección de personas con YOLO.

## Tecnologías

- Python 3.11+
- FastAPI
- Uvicorn
- Ultralytics YOLO
- OpenCV
- NumPy
- Pytest

## Estructura del Proyecto

```
backend/
├── app/
│   ├── main.py              # Aplicación FastAPI principal
│   ├── config.py            # Configuración centralizada
│   ├── api/
│   │   └── routes.py        # Endpoints HTTP
│   ├── services/
│   │   └── detector.py      # Lógica de detección YOLO
│   └── schemas/
│       └── detection.py     # Schemas Pydantic
├── tests/
│   ├── conftest.py          # Fixtures compartidas
│   ├── test_detector.py     # Tests de detección
│   └── test_api.py          # Tests de API
├── scripts/
│   └── run_poc.py           # Script POC Fase 1
├── models/                   # Modelos YOLO (descargados automáticamente)
├── data/
│   └── samples/             # Imágenes de test
├── requirements.txt          # Dependencias Python
├── pytest.ini               # Configuración pytest
├── .env.example             # Variables de entorno ejemplo
└── .env                     # Variables de entorno (gitignored)
```

## Instalación

### Prerrequisitos
- Python 3.11+
- pip

```bash
cd backend

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Configuración

Crea un archivo `.env` basado en `.env.example`:

```bash
cp .env.example .env
```

Variables de entorno configurables:

```env
CONFIDENCE_THRESHOLD=0.50      # Umbral de confianza (0.0 - 1.0)
MODEL_NAME=yolov8n.pt          # Modelo YOLO a usar
MAX_UPLOAD_MB=10               # Tamaño máximo de upload (MB)
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173  # Orígenes permitidos
```

## Ejecución

### Iniciar Servidor de Desarrollo

```bash
cd backend
.venv\Scripts\activate  # Windows
uvicorn app.main:app --reload
```

El servidor estará disponible en http://localhost:8000

### Ejecutar Tests

```bash
cd backend
.venv\Scripts\activate  # Windows
pytest
```

### Ejecutar Script POC (Fase 1)

```bash
cd backend
.venv\Scripts\activate  # Windows
python scripts/run_poc.py [ruta_imagen]
```

Si no se proporciona una imagen, se descargará una de ejemplo automáticamente.

## API Endpoints

### GET /health

Health check del servidor.

**Response**:
```json
{
  "status": "ok"
}
```

### POST /detect

Detecta personas en una imagen.

**Request**: Multipart form-data con archivo de imagen

**Response**:
```json
{
  "total_people": 3,
  "detections": [
    {
      "class_name": "person",
      "confidence": 0.94,
      "bounding_box": {
        "x1": 120,
        "y1": 80,
        "x2": 180,
        "y2": 260
      }
    }
  ],
  "image_result": "base64_encoded_jpeg"
}
```

**Formatos de imagen permitidos**:
- JPG/JPEG
- PNG
- WEBP

**Tamaño máximo**: 10MB (configurable)

## Detalles de Detección

### Modelo YOLO
- **Modelo**: YOLOv8n (nano)
- **Dataset**: COCO (preentrenado)
- **Clase person**: ID 0
- **Umbral de confianza**: 0.50 (configurable)

### Filtrado de Clases
El sistema filtra explícitamente por la clase `person` (class_id = 0 en COCO). Otros objetos (autos, motos, bicicletas, etc.) son ignorados.

### Procesamiento de Imágenes
- Procesamiento en memoria (no guarda archivos en disco)
- La imagen original no se modifica
- La imagen de resultado se codifica en base64 JPEG

## Tests

El backend incluye 14 tests:

**Detector Tests (7 tests)**:
- Detección de personas en imágenes con personas
- Conteo cero en imágenes sin personas
- Vehículos sin personas cuentan cero
- Escenas mixtas cuentan solo personas
- Validación de imágenes inválidas
- Filtrado por umbral de confianza
- La imagen original no se modifica

**API Tests (7 tests)**:
- Health check
- Detección de personas
- Cero personas no es error
- Rechazo de archivo vacío
- Rechazo de extensión inválida
- Rechazo de imagen corrupta
- Rechazo de archivo sobredimensionado

## Variables de Entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| CONFIDENCE_THRESHOLD | 0.50 | Umbral de confianza para detecciones |
| MODEL_NAME | yolov8n.pt | Nombre del modelo YOLO |
| MAX_UPLOAD_MB | 10 | Tamaño máximo de upload en MB |
| CORS_ORIGINS | http://localhost:5173,http://127.0.0.1:5173 | Orígenes permitidos para CORS |

## Consideraciones Importantes

1. **Solo detecta personas**: El sistema filtra exclusivamente por clase person
2. **Modelo ligero**: YOLOv8n para ejecución en CPU sin GPU dedicada
3. **Sin base de datos**: Proyecto académico stateless
4. **Sin autenticación**: Proyecto local sin seguridad adicional
5. **Procesamiento en memoria**: No guarda uploads en disco

## Dependencias

```
ultralytics>=8.3.0
opencv-python>=4.10.0
numpy>=2.0.0
fastapi>=0.115.0
uvicorn>=0.32.0
python-multipart>=0.0.12
httpx>=0.28.0
pytest>=8.0.0
```
