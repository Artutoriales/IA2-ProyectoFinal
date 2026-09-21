import { useEffect, useRef, useState } from 'react';
import { detectPeople } from '../services/api';
import type { DetectionResponse } from '../types/detection';

interface CameraViewProps {
  onDetectionResult: (result: DetectionResponse) => void;
  onError: (error: string) => void;
}

const CAPTURE_INTERVAL = 1000; // 1 segundo entre capturas

export default function CameraView({ onDetectionResult, onError }: CameraViewProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const [isActive, setIsActive] = useState(false);
  const intervalRef = useRef<number | null>(null);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment' },
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setIsStreaming(true);
      }
    } catch (error) {
      onError(
        error instanceof Error
          ? error.message
          : 'No se pudo acceder a la cámara. Verifica los permisos.'
      );
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach((track) => track.stop());
      videoRef.current.srcObject = null;
    }
    setIsStreaming(false);
    setIsActive(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  const captureFrame = () => {
    if (!videoRef.current || !canvasRef.current || !isStreaming) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    if (!context) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);

    canvas.toBlob(async (blob) => {
      if (!blob) return;

      const file = new File([blob], 'camera-frame.jpg', { type: 'image/jpeg' });

      try {
        const result = await detectPeople(file);
        onDetectionResult(result);
      } catch (error) {
        // No mostrar error en cada frame, solo en consola
        console.error('Error al procesar frame:', error);
      }
    }, 'image/jpeg', 0.8);
  };

  const startDetection = () => {
    setIsActive(true);
    intervalRef.current = window.setInterval(captureFrame, CAPTURE_INTERVAL);
  };

  const stopDetection = () => {
    setIsActive(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  return (
    <div className="camera-view">
      <div className="camera-container">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="camera-video"
        />
        <canvas ref={canvasRef} className="camera-canvas" style={{ display: 'none' }} />
      </div>

      <div className="camera-controls">
        {!isStreaming ? (
          <button onClick={startCamera} className="camera-button">
            Iniciar cámara
          </button>
        ) : (
          <>
            {!isActive ? (
              <button onClick={startDetection} className="camera-button start">
                Iniciar detección
              </button>
            ) : (
              <button onClick={stopDetection} className="camera-button stop">
                Pausar detección
              </button>
            )}
            <button onClick={stopCamera} className="camera-button stop">
              Detener cámara
            </button>
          </>
        )}
      </div>

      {isActive && (
        <div className="camera-status">
          <span className="status-indicator" />
          Detectando personas...
        </div>
      )}
    </div>
  );
}
