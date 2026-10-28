import { useRef, useState } from 'react'

const ACCEPTED_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/bmp']
const MAX_MB = 10

export default function UploadZone({ file, previewUrl, onSelect, onClear, disabled }) {
  const inputRef = useRef(null)
  const [dragging, setDragging] = useState(false)
  const [warning, setWarning] = useState(null)

  function validate(candidate) {
    if (!candidate) return 'Không tìm thấy file. Vui lòng chọn lại ảnh.'
    if (!ACCEPTED_TYPES.includes(candidate.type)) {
      return 'Chỉ chấp nhận ảnh định dạng JPG, PNG, WebP hoặc BMP.'
    }
    if (candidate.size > MAX_MB * 1024 * 1024) {
      return `Ảnh quá lớn (tối đa ${MAX_MB}MB).`
    }
    return null
  }

  function handleFileList(files) {
    if (disabled) return
    const candidate = files && files[0]
    const err = validate(candidate)
    setWarning(err)
    if (!err) onSelect(candidate)
  }

  function handleDrop(event) {
    event.preventDefault()
    setDragging(false)
    handleFileList(event.dataTransfer.files)
  }

  function openPicker() {
    if (!disabled && inputRef.current) inputRef.current.click()
  }

  return (
    <div className="panel">
      <div className="panel-label">Ảnh đầu vào</div>
      <div
        className={`dropzone${dragging ? ' dragging' : ''}`}
        onClick={openPicker}
        onDragOver={(e) => {
          e.preventDefault()
          if (!disabled) setDragging(true)
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === 'Enter') openPicker()
        }}
      >
        {previewUrl ? (
          <img src={previewUrl} alt="Ảnh xem trước" />
        ) : (
          <p className="placeholder">
            Nhấn để chọn ảnh X-quang
            <br />
            hoặc kéo thả ảnh vào đây
            <br />
            <small>(JPG/PNG, tối đa {MAX_MB}MB)</small>
          </p>
        )}
      </div>
      <input
        ref={inputRef}
        type="file"
        accept={ACCEPTED_TYPES.join(',')}
        hidden
        onChange={(e) => {
          handleFileList(e.target.files)
          e.target.value = ''
        }}
      />
      {warning && <p className="warning">⚠️ {warning}</p>}
      {file && !warning && (
        <button className="btn-link" onClick={() => !disabled && onClear()}>
          🗑️ Bỏ ảnh đã chọn
        </button>
      )}
    </div>
  )
}
