import React, { useState, useRef } from 'react';

export function UploadPanel({ onUploadSuccess }) {
  const [status, setStatus] = useState('idle');
  const [message, setMessage] = useState('');
  const fileInputRef = useRef(null);

  const processFile = async (file) => {
    if (!file) return;

    const allowedExtensions = ['.pdf', '.txt', '.md'];
    const extension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();

    if (!allowedExtensions.includes(extension)) {
      setStatus('error');
      setMessage('Unsupported file type.');
      return;
    }

    setStatus('uploading');
    setMessage('Uploading...');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const API_BASE = import.meta.env.VITE_API_URL || '';
      const response = await fetch(`${API_BASE}/api/upload`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setStatus('success');
        setMessage('Success');
        if (onUploadSuccess) onUploadSuccess();
        
        setTimeout(() => {
          setStatus('idle');
          setMessage('');
        }, 3000);
      } else {
        setStatus('error');
        setMessage('Upload failed');
        setTimeout(() => setStatus('idle'), 3000);
      }
    } catch (err) {
      console.error(err);
      setStatus('error');
      setMessage('Network error');
      setTimeout(() => setStatus('idle'), 3000);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  const onButtonClick = () => {
    if (status === 'idle' || status === 'error') {
      fileInputRef.current.click();
    }
  };

  let icon = 'upload';
  let text = 'Upload Document';
  if (status === 'uploading') {
    icon = 'sync';
    text = 'Uploading...';
  } else if (status === 'success') {
    icon = 'check_circle';
    text = 'Success';
  } else if (status === 'error') {
    icon = 'error';
    text = message || 'Error';
  }

  return (
    <>
      <input
        ref={fileInputRef}
        type="file"
        className="hidden"
        accept=".pdf,.txt,.md"
        onChange={handleChange}
        disabled={status === 'uploading'}
      />
      <button
        onClick={onButtonClick}
        disabled={status === 'uploading'}
        className={`w-full py-2 px-4 rounded font-label-caps text-label-caps transition-colors flex items-center justify-center gap-2 ${
          status === 'error' 
            ? 'bg-error text-on-error hover:bg-error/80' 
            : status === 'success'
            ? 'bg-secondary text-on-secondary hover:bg-secondary/80'
            : 'bg-primary text-on-primary hover:bg-primary-fixed-dim'
        } ${status === 'uploading' ? 'opacity-70 cursor-not-allowed' : ''}`}
      >
        <span className={`material-symbols-outlined text-sm ${status === 'uploading' ? 'animate-spin' : ''}`}>
          {icon}
        </span>
        {text}
      </button>
    </>
  );
}

export default UploadPanel;
