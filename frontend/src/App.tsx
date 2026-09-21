import { useState } from 'react';
import ImageUploader from './components/ImageUploader';
import CameraView from './components/CameraView';
import DetectionResult from './components/DetectionResult';
import ErrorDisplay from './components/ErrorDisplay';
import { detectPeople } from './services/api';
import type { DetectionResponse } from './types/detection';
import './App.css';

type Mode = 'image' | 'camera';

function App() {
  const [mode, setMode] = useState<Mode>('image');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DetectionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleImageSelect = (file: File) => {
    setSelectedFile(file);
    setResult(null);
    setError(null);

    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  };

  const handleDetect = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);

    try {
      const detectionResult = await detectPeople(selectedFile);
      setResult(detectionResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setLoading(false);
    }
  };

  const handleCameraDetection = (detectionResult: DetectionResponse) => {
    setResult(detectionResult);
  };

  const handleCameraError = (errorMessage: string) => {
    setError(errorMessage);
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
  };

  const handleModeChange = (newMode: Mode) => {
    setMode(newMode);
    handleReset();
  };

  const handleDismissError = () => {
    setError(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Pedestrian Counter YOLO</h1>
        <p>Detecta y cuenta personas mediante inteligencia artificial</p>
      </header>

      <main className="app-main">
        <div className="mode-selector">
          <button
            onClick={() => handleModeChange('image')}
            className={`mode-button ${mode === 'image' ? 'active' : ''}`}
          >
            Subir imagen
          </button>
          <button
            onClick={() => handleModeChange('camera')}
            className={`mode-button ${mode === 'camera' ? 'active' : ''}`}
          >
            Usar cámara
          </button>
        </div>

        {mode === 'image' && (
          <>
            {!previewUrl && !result && (
              <div className="upload-section">
                <ImageUploader
                  onImageSelect={handleImageSelect}
                  disabled={loading}
                />
              </div>
            )}

            {previewUrl && !result && (
              <div className="preview-section">
                <div className="preview-image">
                  <img src={previewUrl} alt="Vista previa" />
                </div>
                <div className="preview-actions">
                  <button
                    onClick={handleDetect}
                    disabled={loading}
                    className="detect-button"
                  >
                    {loading ? 'Analizando...' : 'Analizar imagen'}
                  </button>
                  <button
                    onClick={handleReset}
                    disabled={loading}
                    className="reset-button"
                  >
                    Cancelar
                  </button>
                </div>
              </div>
            )}
          </>
        )}

        {mode === 'camera' && !result && (
          <div className="camera-section">
            <CameraView
              onDetectionResult={handleCameraDetection}
              onError={handleCameraError}
            />
          </div>
        )}

        {result && (
          <div className="result-section">
            <DetectionResult result={result} />
            <button onClick={handleReset} className="new-image-button">
              {mode === 'image' ? 'Analizar otra imagen' : 'Continuar con cámara'}
            </button>
          </div>
        )}

        {error && (
          <ErrorDisplay error={error} onDismiss={handleDismissError} />
        )}
      </main>
    </div>
  );
}

export default App;
