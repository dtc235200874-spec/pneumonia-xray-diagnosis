import { useEffect, useState } from 'react'
import ConfidenceChart from './components/ConfidenceChart.jsx'
import ResultPanel from './components/ResultPanel.jsx'
import UploadZone from './components/UploadZone.jsx'
import { predictImage } from './api.js'

export default function App() {
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [result, setResult] = useState(null)
  const [status, setStatus] = useState('idle') // idle | loading | done | error
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!file) {
      setPreviewUrl(null)
      return undefined
    }
    const url = URL.createObjectURL(file)
    setPreviewUrl(url)
    return () => URL.revokeObjectURL(url)
  }, [file])

  async function handlePredict() {
    if (!file || status === 'loading') return
    setStatus('loading')
    setError(null)
    try {
      const data = await predictImage(file)
      setResult(data)
      setStatus('done')
    } catch (err) {
      setResult(null)
      setError(err.message || 'Có lỗi xảy ra khi phân tích ảnh.')
      setStatus('error')
    }
  }

  function handleClear() {
    setFile(null)
    setResult(null)
    setError(null)
    setStatus('idle')
  }

  const isLoading = status === 'loading'

  return (
    <div className="app">
      <h1 className="title">🩺 CHẨN ĐOÁN VIÊM PHỔI (X-QUANG)</h1>
      <p className="subtitle">Phân tích ảnh X-quang bằng YOLOv8 — giao diện React</p>

      <div className="grid">
        <UploadZone
          file={file}
          previewUrl={previewUrl}
          onSelect={setFile}
          onClear={handleClear}
          disabled={isLoading}
        />
        <div className="panel">
          <div className="panel-label">Kết quả</div>
          {result ? (
            <img src={result.annotated_image} alt="Ảnh kết quả" />
          ) : (
            <p className="placeholder">
              {isLoading ? '⏳ Đang phân tích ảnh...' : 'Ảnh kết quả sẽ hiển thị ở đây'}
            </p>
          )}
        </div>
      </div>

      <ResultPanel status={status} result={result} error={error} />

      <div className="actions">
        <button className="btn btn-primary" onClick={handlePredict} disabled={!file || isLoading}>
          {isLoading ? '⏳ Đang phân tích...' : '🚀 Dự đoán'}
        </button>
        <button className="btn btn-secondary" onClick={handleClear} disabled={isLoading}>
          🧹 Xóa và làm lại
        </button>
      </div>

      {result && (
        <div className="chart-wrap">
          <h3 className="chart-title">📊 Độ tin cậy mô hình</h3>
          <ConfidenceChart probabilities={result.probabilities} />
        </div>
      )}

      <p className="disclaimer">
        ⚕️ Kết quả chỉ mang tính tham khảo, không thay thế chẩn đoán của bác sĩ.
      </p>
    </div>
  )
}
