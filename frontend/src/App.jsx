import { useState, useRef } from 'react'
import axios from 'axios'
import { Upload, Music, Mic, Layers, Download } from 'lucide-react'
import './index.css'

function App() {
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const fileInputRef = useRef(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
      setPreviewUrl(URL.createObjectURL(selectedFile))
      setResult(null)
      setError(null)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const selectedFile = e.dataTransfer.files[0]
    if (selectedFile && (selectedFile.type.startsWith('audio/') || selectedFile.type.startsWith('video/'))) {
      setFile(selectedFile)
      setPreviewUrl(URL.createObjectURL(selectedFile))
      setResult(null)
      setError(null)
    }
  }

  const processAudio = async () => {
    if (!file) return

    setIsProcessing(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      // Ajusta la URL del backend si es necesario
      const response = await axios.post('http://localhost:8069/separate/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setResult(response.data)
    } catch (err) {
      console.error(err);
      setError('Ocurrió un error procesando tu archivo. Inténtalo de nuevo.')
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <div className="container">
      <div className="glass-card">
        <h1>PrismAudio</h1>
        <p className="subtitle">Separa la voz y la música con Inteligencia Artificial</p>

        {!result && (
          <div
            className={`upload-area ${file ? 'active' : ''}`}
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              style={{ display: 'none' }}
              accept="audio/*,video/*"
            />

            {file ? (
              <div>
                <Music className="upload-icon" />
                <div className="upload-text">{file.name}</div>
                <div className="upload-subtext">{(file.size / 1024 / 1024).toFixed(2)} MB</div>
              </div>
            ) : (
              <div>
                <Upload className="upload-icon" />
                <div className="upload-text">Arrastra tu archivo aquí o haz clic</div>
                <div className="upload-subtext">Soporta MP3, MP4, WAV</div>
              </div>
            )}
          </div>
        )}

        {error && (
          <div style={{ color: '#ff4d4d', marginTop: '1rem', background: 'rgba(255,0,0,0.1)', padding: '0.5rem', borderRadius: '8px' }}>
            {error}
          </div>
        )}

        {file && !result && (
          <button
            className="btn"
            onClick={processAudio}
            disabled={isProcessing}
          >
            {isProcessing ? 'Procesando...' : 'Separar Audio'}
          </button>
        )}

        {isProcessing && (
          <div className="loader"></div>
        )}

        {result && (
          <div className="result-section">
            <h3 style={{ marginBottom: '1.5rem', fontSize: '1.5rem' }}>Resultados para: {result.original}</h3>

            {/* Vocals Track */}
            <div className="track-card">
              <div className="track-icon">
                <Mic size={24} />
              </div>
              <div className="track-info">
                <span className="track-name">Voz (Vocals)</span>
                <audio controls src={`http://localhost:8069${result.vocals_url}`} />
              </div>
              <a href={`http://localhost:8069${result.vocals_url}`} download className="btn" style={{ padding: '0.5rem 1rem', marginTop: 0, fontSize: '0.9rem' }}>
                <Download size={18} />
              </a>
            </div>

            {/* Accompaniment Track */}
            <div className="track-card">
              <div className="track-icon" style={{ background: 'linear-gradient(135deg, #00c6ff, #0072ff)' }}>
                <Layers size={24} />
              </div>
              <div className="track-info">
                <span className="track-name">Instrumental (Accompaniment)</span>
                <audio controls src={`http://localhost:8069${result.accompaniment_url}`} />
              </div>
              <a href={`http://localhost:8069${result.accompaniment_url}`} download className="btn" style={{ padding: '0.5rem 1rem', marginTop: 0, fontSize: '0.9rem' }}>
                <Download size={18} />
              </a>
            </div>

            <button
              className="btn"
              onClick={() => { setFile(null); setResult(null); }}
              style={{ background: 'transparent', border: '1px solid var(--border-color)', marginTop: '2rem' }}
            >
              Procesar otro archivo
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
