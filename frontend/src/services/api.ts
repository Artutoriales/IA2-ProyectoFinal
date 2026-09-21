import type { DetectionResponse, HealthResponse } from '../types/detection';

const API_BASE_URL = 'http://localhost:8000';

export async function checkHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) {
    throw new Error('Error al verificar estado del servidor');
  }
  return response.json();
}

export async function detectPeople(imageFile: File): Promise<DetectionResponse> {
  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await fetch(`${API_BASE_URL}/detect`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Error desconocido' }));
    throw new Error(errorData.detail || 'Error al procesar la imagen');
  }

  return response.json();
}
