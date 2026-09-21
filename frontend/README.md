# Frontend - Pedestrian Counter YOLO

Frontend React + TypeScript para el sistema de detección de personas con YOLO.

## Tecnologías

- React 19
- TypeScript
- Vite
- Bun (package manager)

## Estructura del Proyecto

```
frontend/
├── src/
│   ├── components/
│   │   ├── ImageUploader.tsx    # Componente para subir imágenes
│   │   ├── DetectionResult.tsx  # Componente para mostrar resultados
│   │   └── ErrorDisplay.tsx     # Componente para mostrar errores
│   ├── services/
│   │   └── api.ts               # Servicio de comunicación con backend
│   ├── types/
│   │   └── detection.ts         # Tipos TypeScript para la API
│   ├── App.tsx                  # Componente principal
│   ├── App.css                  # Estilos principales
│   ├── main.tsx                 # Punto de entrada
│   └── index.css                # Estilos globales
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## Instalación

### Prerrequisitos
- Bun (instalar con `npm install -g bun` si no está disponible)

```bash
cd frontend
bun install
```

## Desarrollo

```bash
bun run dev
```

El frontend estará disponible en http://localhost:5173

## Build

```bash
bun run build
```

## Preview del Build

```bash
bun run preview
```

## Configuración

El frontend se comunica con el backend en `http://localhost:8000` por defecto. Para cambiar esto, modifica `src/services/api.ts`:

```typescript
const API_BASE_URL = 'http://localhost:8000';
```

## Funcionalidades

- **Modo Imagen**:
  - Subida de imágenes (JPG, PNG, WEBP)
  - Preview de la imagen seleccionada
  - Análisis de la imagen con YOLO
  - Display de resultados con imagen anotada

- **Modo Cámara**:
  - Acceso a cámara del navegador
  - Preview de cámara en tiempo real
  - Captura de frames a intervalos (1 segundo)
  - Detección en tiempo real
  - Control de start/stop
  - Indicador de estado de detección

- **Display de Resultados**:
  - Imagen anotada con bounding boxes
  - Conteo de personas
  - Lista de detecciones con confianza

- **General**:
  - Manejo de errores
  - UI en español
  - Diseño responsive

## Backend Requerido

El frontend requiere que el backend esté ejecutándose en `http://localhost:8000`. Para iniciar el backend:

```bash
cd backend
.venv/Scripts/activate  # Windows
uvicorn app.main:app --reload
```

## API Response

El backend devuelve:

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
