interface ErrorDisplayProps {
  error: string;
  onDismiss: () => void;
}

export default function ErrorDisplay({ error, onDismiss }: ErrorDisplayProps) {
  return (
    <div className="error-display">
      <div className="error-content">
        <h3>Error</h3>
        <p>{error}</p>
        <button onClick={onDismiss} className="dismiss-button">
          Cerrar
        </button>
      </div>
    </div>
  );
}
