# Pedestrian Counter YOLO

Sistema académico de visión por computador para detectar y contar **exclusivamente personas** en imágenes de cruces peatonales mediante YOLO.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![React](https://img.shields.io/badge/React-19-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-6.0-blue)
![YOLO](https://img.shields.io/badge/YOLO-v8.3.0-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green)

## 🎯 Objetivo

Este proyecto es un sistema académico de Inteligencia Artificial que utiliza YOLO (You Only Look Once) para detectar y contar personas en imágenes o video en tiempo real. El sistema está diseñado para cruces peatonales y cuenta **exclusivamente personas**, ignorando otros objetos como autos, motos, bicicletas, etc.

## ✨ Características

- **Detección de personas**: Usa YOLOv8n preentrenado en COCO
- **Filtrado exclusivo**: Solo detecta la clase `person` (class_id = 0)
- **Dos modos de operación**:
  - 📷 **Modo Imagen**: Subida y análisis de imágenes estáticas
  - 🎥 **Modo Cámara**: Detección en tiempo real con webcam
- **API REST**: Backend FastAPI con endpoints de detección
- **Frontend React**: Interfaz moderna con TypeScript
- **Resultados visuales**: Imagen anotada con bounding boxes y conteo
- **Configuración flexible**: Umbral de confianza ajustable

## 🏗️ Arquitectura

```
IA2-ProyectoFinal/
├── backend/                 # Backend Python/FastAPI
│   ├── app/
│   │   ├── main.py          # Aplicación FastAPI
│   │   ├── config.py        # Configuración
│   │   ├── api/routes.py    # Endpoints
│   │   ├── services/detector.py  # Lógica YOLO
│   │   └── schemas/detection.py  # Schemas
│   ├── tests/               # Tests (14 tests)
│   ├── scripts/             # Scripts utilitarios
│   ├── models/              # Modelos YOLO
│   └── requirements.txt     # Dependencias
├── frontend/                # Frontend React/TypeScript
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── services/        # Servicio API
│   │   ├── types/           # Tipos TypeScript
│   │   └── App.tsx          # Aplicación principal
│   └── package.json         # Dependencias
├── AGENTS.md                # Documentación para agentes
├── PROJECT_STATUS.md        # Estado del proyecto
└── README.md                # Este archivo
```

## 🚀 Requisitos Previos

### Backend
- Python 3.11+
- pip

### Frontend
- Bun (instalar con `npm install -g bun` si no está disponible)
- Navegador web moderno

## 📦 Instalación y Ejecución

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Artutoriales/IA2-ProyectoFinal.git
cd IA2-ProyectoFinal
```

### 2. Configurar el Backend

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

# Configurar variables de entorno
cp .env.example .env
# Editar .env si necesitas cambiar configuración
```

### 3. Configurar el Frontend

```bash
cd frontend

# Instalar dependencias (usar Bun)
bun install
```

### 4. Iniciar los Servidores

**Terminal 1 - Backend**:
```bash
cd backend
.venv\Scripts\activate  # Windows
uvicorn app.main:app --reload
```

El backend estará disponible en http://localhost:8000

**Terminal 2 - Frontend**:
```bash
cd frontend
bun run dev
```

El frontend estará disponible en http://localhost:5173

### 5. Abrir la Aplicación

Abre tu navegador en http://localhost:5173

## 🎮 Uso de la Aplicación

### Modo Imagen
1. Selecciona "Subir imagen"
2. Elige una imagen (JPG, PNG, WEBP)
3. Haz clic en "Analizar imagen"
4. Visualiza los resultados:
   - Imagen anotada con bounding boxes
   - Conteo total de personas
   - Lista de detecciones con confianza

### Modo Cámara
1. Selecciona "Usar cámara"
2. Haz clic en "Iniciar cámara"
3. Otorga permisos de cámara cuando se soliciten
4. Haz clic en "Iniciar detección"
5. El sistema captura frames cada 1 segundo
6. Visualiza los resultados en tiempo real

## 🧪 Tests

### Backend Tests

```bash
cd backend
.venv\Scripts\activate  # Windows
pytest
```

El backend incluye 14 tests que verifican:
- Detección de personas
- Filtrado de clase person
- Validación de uploads
- Manejo de errores

## 🔧 Configuración

### Backend (.env)

```env
CONFIDENCE_THRESHOLD=0.50      # Umbral de confianza (0.0 - 1.0)
MODEL_NAME=yolov8n.pt          # Modelo YOLO
MAX_UPLOAD_MB=10               # Tamaño máximo de upload (MB)
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Frontend (src/services/api.ts)

```typescript
const API_BASE_URL = 'http://localhost:8000';
```

## 📊 API Endpoints

### GET /health
Health check del servidor.

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

## 🛠️ Tecnologías

### Backend
- Python 3.11+
- FastAPI
- Uvicorn
- Ultralytics YOLOv8n
- OpenCV
- NumPy
- Pytest

### Frontend
- React 19
- TypeScript
- Vite
- Bun (package manager)

## 📈 Estado del Proyecto

- **Fase 1**: ✅ YOLO Proof of Concept
- **Fase 2**: ✅ Detection Service
- **Fase 3**: ✅ FastAPI Backend
- **Fase 4**: ✅ React Frontend (Modo Imagen)
- **Fase 5**: ✅ Webcam (Modo Cámara)
- **Fase 6**: ⏳ Evaluación Académica
- **Fase 7**: ⏳ Presentación Académica

Para más detalles sobre el estado del proyecto, consulta [PROJECT_STATUS.md](PROJECT_STATUS.md).

## 📚 Documentación Adicional

- [AGENTS.md](AGENTS.md) - Documentación para agentes de programación
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - Estado detallado del proyecto
- [backend/README.md](backend/README.md) - Documentación del backend
- [frontend/README.md](frontend/README.md) - Documentación del frontend

## ⚠️ Consideraciones Importantes

1. **Solo detecta personas**: El sistema filtra exclusivamente por clase person
2. **Modelo ligero**: YOLOv8n para ejecución en CPU sin GPU dedicada
3. **Sin base de datos**: Proyecto académico stateless
4. **Sin autenticación**: Proyecto local sin seguridad adicional
5. **Procesamiento en memoria**: No guarda uploads en disco

## 🤝 Contribuciones

Este es un proyecto académico. Las contribuciones deben seguir las reglas establecidas en [AGENTS.md](AGENTS.md).

## 📄 Licencia

Este proyecto es académico y educativo.

## 👨‍🏫 Uso Académico

Este proyecto está diseñado para presentaciones académicas sobre:
- Visión por computador
- Detección de objetos con YOLO
- Aplicaciones de IA en sistemas de transporte
- Desarrollo de sistemas full-stack con Python y React

---

**Desarrollado para el curso de Inteligencia Artificial**

