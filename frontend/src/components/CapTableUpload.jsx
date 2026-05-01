import React, { useState } from 'react';
import '../styles/components.css';

const CapTableUpload = ({ onUploadSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLoadSample = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('http://localhost:8000/load-sample-data', {
        method: 'POST',
      });
      const result = await response.json();
      if (result.success) {
        onUploadSuccess(result.data);
      }
    } catch (err) {
      setError('Failed to load sample data: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleJsonUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (event) => {
      try {
        const data = JSON.parse(event.target.result);
        setLoading(true);
        const response = await fetch('http://localhost:8000/upload-cap-table-json', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        });
        const result = await response.json();
        if (result.success) {
          onUploadSuccess(data);
        } else {
          setError('Upload failed: ' + result.detail);
        }
      } catch (err) {
        setError('Invalid JSON or upload error: ' + err.message);
      } finally {
        setLoading(false);
      }
    };
    reader.readAsText(file);
  };

  return (
    <div className="upload-container">
      <h2>📊 Cap Table Upload</h2>
      <div className="button-group">
        <button 
          onClick={handleLoadSample} 
          disabled={loading}
          className="btn btn-primary"
        >
          {loading ? 'Loading...' : '📋 Load Sample Data'}
        </button>
        <label className="btn btn-secondary">
          📁 Upload JSON
          <input 
            type="file" 
            accept=".json" 
            onChange={handleJsonUpload}
            disabled={loading}
            style={{ display: 'none' }}
          />
        </label>
      </div>
      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

export default CapTableUpload;
