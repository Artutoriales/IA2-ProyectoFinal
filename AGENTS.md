# AGENTS.md - Contexto para Agentes de Programación

## Objetivo del Proyecto

Sistema académico de visión por computador para detectar y contar **exclusivamente personas** en imágenes de cruces peatonales mediante YOLO.

## Restricción Crítica

**Solo se deben detectar y contar personas.** Otros objetos (autos, motos, bicicletas, perros, señales de tráfico, etc.) deben ser ignorados por el sistema.

## Arquitectura Actual

### Backend (Python/FastAPI)
- **Framework**: FastAPI con Uvicorn
- **Modelo**: YOLOv8n (preentrenado en COCO)
- **Procesamiento de imágenes**: OpenCV + NumPy
- **Estructura**:
  - `backend/app/main.py` - Aplicación FastAPI principal
  - `backend/app/config.py` - Configuración centralizada
  - `backend/app/api/routes.py` - Endpoints HTTP
  - `backend/app/services/detector.py` - Lógica de detección YOLO
  - `backend/app/schemas/detection.py` - Schemas Pydantic

### Frontend
**No implementado aún** - Pendiente Fase 4

## Estado Actual del Proyecto

### Fases Completadas
- **Fase 1**: YOLO proof of concept ✓
  - Script: `backend/scripts/run_poc.py`
  - Carga modelo, detecta personas, muestra conteo
- **Fase 2**: Detection service ✓
  - Servicio modular en `detector.py`
  - Configuración centralizada
  - Tests unitarios en `test_detector.py`
- **Fase 3**: FastAPI ✓
  - Endpoint `/health`
  - Endpoint `/detect` (POST)
  - Validación de uploads
  - Tests de API en `test_api.py`

### Fases Pendientes
- **Fase 4**: React frontend (próxima fase)
- **Fase 5**: Webcam
- **Fase 6**: Evaluación académica
- **Fase 7**: Presentación

## Tecnologías Utilizadas

### Backend
- Python 3.11+
- ultralytics>=8.3.0
- opencv-python>=4.10.0
- numpy>=2.0.0
- fastapi>=0.115.0
- uvicorn>=0.32.0
- python-multipart>=0.0.12
- httpx>=0.28.0
- pytest>=8.0.0

### Frontend (cuando se implemente)
- React
- TypeScript
- Vite
- **Bun** (NO usar npm)

## Configuración del Backend

### Variables de Entorno (.env)
```
CONFIDENCE_THRESHOLD=0.50
MODEL_NAME=yolov8n.pt
MAX_UPLOAD_MB=10
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Clase Person en COCO
- `PERSON_CLASS_ID = 0`
- `PERSON_CLASS_NAME = "person"`

### Formatos de Imagen Permitidos
- Extensiones: .jpg, .jpeg, .png, .webp
- MIME types: image/jpeg, image/jpg, image/png, image/webp
- Tamaño máximo: 10MB (configurable)

## Endpoints API

### GET /health
```json
{
  "status": "ok"
}
```

### POST /detect
**Input**: Multipart form-data con archivo de imagen

**Output**:
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

## Lógica de Detección

### Filtrado de Clases
El sistema filtra explícitamente por `PERSON_CLASS_ID = 0`:
```python
results = get_model().predict(
    source=image,
    conf=threshold,
    classes=[PERSON_CLASS_ID],  # Solo clase person
    verbose=False,
)
```

### Umbral de Confianza
- Default: 0.50
- Configurable vía variable de entorno
- Aumentar reduce falsos positivos pero puede omitir personas reales

### Procesamiento de Imágenes
- OpenCV para lectura/decodificación
- No se guardan archivos subidos en disco (procesamiento en memoria)
- La imagen original no se modifica (se crea copia para anotaciones)
- Resultado codificado en base64 JPEG

## Tests

### Detector Tests (`test_detector.py`)
- Detección de personas en imágenes con personas
- Conteo cero en imágenes sin personas
- Vehículos sin personas cuentan cero
- Escenas mixtas cuentan solo personas
- Validación de imágenes inválidas
- Filtrado por umbral de confianza
- La imagen original no se modifica

### API Tests (`test_api.py`)
- Health check
- Detección de personas
- Detección cero personas (no es error)
- Rechazo de archivo vacío
- Rechazo de extensión inválida
- Rechazo de imagen corrupta
- Rechazo de archivo sobredimensionado

## Comandos Importantes

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
bun install
bun run dev
bun run build
```

### Iniciar Ambos Servidores (Desarrollo)

**Terminal 1 - Backend**:
```bash
cd backend
.venv\Scripts\activate  # Windows
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend**:
```bash
cd frontend
bun run dev
```

### Script POC
```bash
cd backend
python scripts/run_poc.py [ruta_imagen]
```

## Decisiones Técnicas Importantes

1. **Solo clase person**: El sistema filtra explícitamente por `class_id = 0` (person en COCO)
2. **Modelo ligero**: YOLOv8n para ejecución en CPU sin GPU dedicada
3. **Procesamiento en memoria**: No se guardan uploads en disco
4. **Sin base de datos**: Proyecto académico, no requiere persistencia
5. **Sin autenticación**: Proyecto académico local
6. **CORS configurado**: Para frontend en localhost:5173
7. **Configuración centralizada**: Todas las variables en `config.py`
8. **Separación de responsabilidades**: API lógica separada de detección YOLO

## Restricciones de Desarrollo

1. **NO agregar funcionalidades no solicitadas**
2. **NO refactorizar código existente sin necesidad**
3. **NO cambiar dependencias sin aprobación**
4. **NO agregar base de datos**
5. **NO agregar autenticación**
6. **NO agregar Docker**
7. **NO entrenar modelo personalizado**
8. **NO detectar otras clases además de person**
9. **Usar Bun para frontend (NO npm)**
10. **Mantener código simple y académicamente explicable**

## Convenciones de Código

### Python
- PEP 8
- Type hints donde sea útil
- Nombres claros en inglés para código interno
- Nombres en español para UI/usuario
- Docstrings concisos
- Comentarios que explican "por qué", no "qué"

### TypeScript (cuando se implemente)
- Strict typing
- Evitar `any`
- Componentes reutilizables
- Separar llamadas API de UI

## Estructura de Directorios

```
IA2-ProyectoFinal/
├── README.md
├── AGENTS.md
├── PROJECT_STATUS.md
├── .cursorrules
├── .gitignore
└── backend/
    ├── .env.example
    ├── .env (gitignored)
    ├── requirements.txt
    ├── pytest.ini
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── config.py
    │   ├── api/
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   ├── services/
    │   │   ├── __init__.py
    │   │   └── detector.py
    │   └── schemas/
    │       ├── __init__.py
    │       └── detection.py
    ├── tests/
    │   ├── conftest.py
    │   ├── test_detector.py
    │   └── test_api.py
    ├── scripts/
    │   └── run_poc.py
    ├── models/
    │   └── yolov8n.pt (descargado automáticamente)
    ├── data/
    │   └── samples/
    │       └── bus.jpg (descargado para tests)
    ├── output/
    │   └── (resultados de script POC)
    └── .venv/ (gitignored)
```

## Flujo de Trabajo para Nuevas Features

1. Analizar el estado actual del repositorio
2. Identificar la fase actual del proyecto
3. Implementar solo lo necesario para esa fase
4. Escribir/actualizar tests
5. Verificar que no se rompa funcionalidad existente
6. Documentar cambios relevantes

## Errores Comunes a Evitar

1. Detectar/countear otras clases además de person
2. Guardar archivos subidos en disco
3. Modificar la imagen original
4. Hardcodear el umbral de confianza
5. Usar nombres en español en el código interno
6. Usar npm en lugar de Bun para frontend
7. Agregar dependencias innecesarias
8. Hacer commits gigantes con cambios no relacionados
