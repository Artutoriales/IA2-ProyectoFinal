# Reglas Específicas de Devin - IA2-ProyectoFinal

## Regla #1: SOLO Detectar Personas

Este proyecto detecta y cuenta **exclusivamente personas**. No agregar lógica para detectar otros objetos (autos, motos, bicicletas, perros, etc.).

- El filtro por `PERSON_CLASS_ID = 0` (clase person en COCO) es obligatorio
- No modificar el código que filtra por clase person
- No agregar detección de otras clases

## Regla #2: Preservar Funcionalidad Existente

El proyecto está en Fase 3 completada. Antes de modificar código:

1. Leer y entender el código existente
2. Verificar que la modificación no rompe tests existentes
3. Ejecutar `pytest` después de cambios en backend
4. No refactorizar código que funciona sin necesidad

## Regla #3: No Inventar Funcionalidades

Solo implementar lo que está definido en las fases del proyecto:

- Fase 1-3: Completadas ✓
- Fase 4: React frontend (imagen upload)
- Fase 5: Webcam
- Fase 6: Evaluación académica
- Fase 7: Presentación

No agregar features que no estén en estas fases.

## Regla #4: Backend Commands

Para trabajar en el backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

## Regla #5: Frontend Commands (CUANDO se implemente Fase 4)

Para trabajar en el frontend:

```bash
# Usar SIEMPRE Bun, nunca npm
bun install
bun add <paquete>
bun run dev
bun run build
```

## Regla #6: No Modificar Archivos de Configuración Sin Necesidad

No modificar:
- `backend/requirements.txt` (a menos que sea necesario para una nueva feature)
- `backend/.env.example` (solo si se agrega una nueva variable de entorno)
- `backend/pytest.ini`
- `.gitignore`

## Regla #7: Tests

Antes de considerar una tarea completa:

- Ejecutar `pytest` en `backend/`
- Verificar que todos los tests pasen
- Para nuevas funcionalidades, escribir tests primero

## Regla #8: Dependencias

- Python: Solo agregar dependencias que sean absolutamente necesarias
- Frontend: Solo agregar dependencias que sean absolutamente necesarias
- Preferir versiones publicadas hace al menos 7 días
- No usar floating ranges (`latest`, `*`)

## Regla #9: Comentarios

- NO agregar o quitar comentarios del código existente
- Solo agregar comentarios explicativos en código nuevo cuando sea necesario
- Los comentarios deben explicar "por qué", no "qué"

## Regla #10: Convenciones de Nombres

- Código interno: Inglés (`total_people`, `detections`, `confidence`)
- UI/Usuario: Español (`Personas detectadas`, `Confianza`, `Resultado`)
- Schemas Pydantic: Español (`total_personas`, `detecciones`, `caja`)

## Regla #11: Estructura de Archivos

No cambiar la estructura de directorios existente del backend:

```
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── api/routes.py
│   ├── services/detector.py
│   └── schemas/detection.py
├── tests/
│   ├── conftest.py
│   ├── test_detector.py
│   └── test_api.py
├── scripts/
│   └── run_poc.py
└── requirements.txt
```

## Regla #12: Variables de Entorno

- No hardcodear valores configurables
- Usar variables de entorno para configuración
- Agregar nuevas variables a `.env.example`
- Leer configuración desde `app/config.py`

## Regla #13: Procesamiento de Imágenes

- NO guardar archivos subidos en disco
- Procesar imágenes en memoria
- NO modificar la imagen original
- Crear copia para anotaciones
- Usar OpenCV para procesamiento

## Regla #14: API Response Format

Mantener el formato de respuesta actual en `/detect` (nombres en inglés para TypeScript):

```json
{
  "total_people": int,
  "detections": [
    {
      "class_name": "person",
      "confidence": float,
      "bounding_box": {
        "x1": int,
        "y1": int,
        "x2": int,
        "y2": int
      }
    }
  ],
  "image_result": "base64_encoded_jpeg"
}
```

## Regla #15: Errores HTTP

- Cero personas NO es un error → retornar 200 con `total_personas: 0`
- Imagen inválida → 400
- Formato no permitido → 400
- Archivo vacío → 400
- Archivo sobredimensionado → 400

## Regla #16: Modelos YOLO

- NO descargar modelos innecesariamente grandes
- Usar YOLOv8n por defecto (modelo ligero)
- El modelo se descarga automáticamente en `backend/models/`
- No cambiar la configuración del modelo sin aprobación

## Regla #17: CORS

- CORS configurado para `http://localhost:5173` y `http://127.0.0.1:5173`
- No modificar configuración CORS sin necesidad
- Configuración en `app/config.py` y `app/main.py`

## Regla #18: Type Hints

- Python: Usar type hints donde sea útil
- TypeScript (cuando se implemente): Strict typing, evitar `any`

## Regla #19: Git Workflow

- Hacer commits pequeños y significativos
- No hacer commits gigantes con cambios no relacionados
- Usar formato:
  ```
  feat: descripción
  fix: descripción
  test: descripción
  docs: descripción
  ```

## Regla #20: Verificación

Antes de considerar una tarea completa:

1. Leer el código modificado
2. Ejecutar tests relevantes
3. Verificar que no se rompa funcionalidad existente
4. Documentar cambios si es necesario

## Regla #21: Modos del Frontend

El frontend tiene dos modos:
- **Modo Imagen**: Subida y análisis de imágenes estáticas
- **Modo Cámara**: Acceso a webcam con detección en tiempo real

El selector de modo permite cambiar entre ambos.

## Regla #22: Configuración de Webcam

- Intervalo de captura: 1000ms (1 segundo)
- Configurable via CAPTURE_INTERVAL en CameraView.tsx
- No cambiar el intervalo sin necesidad
- Intervalos muy cortos pueden saturar el backend

## Regla #23: Permisos de Cámara

- La cámara requiere permisos del navegador
- Si el usuario deniega permisos, mostrar error claro
- Manejar errores de cámara con mensajes específicos
- No saturar con errores en cada frame fallido

## Regla #21: Fase Actual

El proyecto está en **Fase 3 completada**. La próxima fase es **Fase 4: React frontend**.

No saltar a fases posteriores sin completar la fase actual.

## Regla #22: Preguntas al Usuario

Si hay ambigüedad en una solicitud:

1. Primero intentar interpretar usando el contexto del proyecto
2. Buscar código relacionado en el repositorio
3. Si aún hay incertidumbre, preguntar al usuario de forma específica

## Regla #23: No Modificar README.md

El README.md actual es mínimo. No modificarlo sin aprobación explícita del usuario.

## Regla #24: No Modificar .cursorrules

El archivo .cursorrules contiene las reglas originales del proyecto. No modificarlo.

## Regla #25: Documentación

- Actualizar `AGENTS.md` si se agregan nuevas funcionalidades importantes
- Actualizar `PROJECT_STATUS.md` si cambia el estado del proyecto
- No crear archivos de documentación adicionales sin aprobación

## Regla #26: Security

- No exponer secrets o credenciales
- No commitar archivos .env
- Validar uploads (tipo, tamaño, extensión)
- No ejecutar código subido

## Regla #27: Performance

- Priorizar funcionalidad correcta sobre optimización prematura
- El proyecto debe funcionar en CPU sin GPU dedicada
- No optimizar sin mediciones reales

## Regla #28: Academic Focus

Este es un proyecto académico. El código debe ser:

- Simple y entendible
- Fácil de explicar en una presentación
- Bien comentado para explicar conceptos de IA
- No sobre-ingenierizado

## Regla #29: Scripts

- El script `backend/scripts/run_poc.py` es para pruebas manuales
- No modificarlo sin necesidad
- Sirve para verificar Fase 1

## Regla #30: Error Recovery

Si encuentras errores:

1. Intentar diferentes enfoques
2. Buscar problemas similares en el códigobase
3. Solo pedir ayuda al usuario como último recurso
4. Excepción: Siempre pedir ayuda con problemas de autenticación, configuración de proyecto, o permisos
