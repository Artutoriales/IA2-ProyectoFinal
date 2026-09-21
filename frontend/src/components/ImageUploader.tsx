interface ImageUploaderProps {
  onImageSelect: (file: File) => void;
  disabled: boolean;
}

export default function ImageUploader({ onImageSelect, disabled }: ImageUploaderProps) {
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onImageSelect(file);
    }
  };

  return (
    <div className="image-uploader">
      <input
        type="file"
        id="image-input"
        accept="image/jpeg,image/jpg,image/png,image/webp"
        onChange={handleFileChange}
        disabled={disabled}
        className="file-input"
      />
      <label htmlFor="image-input" className={`upload-button ${disabled ? 'disabled' : ''}`}>
        {disabled ? 'Procesando...' : 'Seleccionar imagen'}
      </label>
    </div>
  );
}
