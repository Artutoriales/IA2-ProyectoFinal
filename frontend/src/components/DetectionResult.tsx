import type { DetectionResponse } from '../types/detection';

interface DetectionResultProps {
  result: DetectionResponse;
}

export default function DetectionResult({ result }: DetectionResultProps) {
  const { total_people, detections, image_result } = result;

  return (
    <div className="detection-result">
      <div className="result-header">
        <h2>Resultado de Detección</h2>
        <div className="people-count">
          <span className="count-number">{total_people}</span>
          <span className="count-label">
            {total_people === 1 ? 'persona detectada' : 'personas detectadas'}
          </span>
        </div>
      </div>

      <div className="result-image">
        <img
          src={`data:image/jpeg;base64,${image_result}`}
          alt="Imagen con detecciones"
          className="annotated-image"
        />
      </div>

      {detections.length > 0 && (
        <div className="detections-list">
          <h3>Detecciones</h3>
          <ul className="detection-items">
            {detections.map((detection, index) => (
              <li key={index} className="detection-item">
                <span className="detection-class">{detection.class_name}</span>
                <span className="detection-confidence">
                  {(detection.confidence * 100).toFixed(1)}%
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
