const LEVEL_EMOJI = { Thấp: '🟡', 'Trung bình': '🟠', Cao: '🔴' }

const LEVEL_COLORS = { Thấp: '#b8860b', 'Trung bình': '#e67e22', Cao: '#d64545' }

export default function ResultPanel({ status, result, error }) {
  if (status === 'error') {
    return <div className="result-box error">⚠️ {error}</div>
  }

  if (!result) {
    return (
      <div className="result-box neutral">
        {status === 'loading' ? '⏳ Đang phân tích, vui lòng đợi...' : 'Kết quả sẽ hiển thị ở đây'}
      </div>
    )
  }

  const { confidence, level, is_pneumonia } = result

  return (
    <div className={`result-box ${is_pneumonia ? 'red' : 'green'}`}>
      {is_pneumonia ? '🔴 VIÊM PHỔI' : '✅ BÌNH THƯỜNG'}
      <br />
      <br />
      Độ tin cậy: <b>{confidence.toFixed(2)}</b>
      <br />
      Mức độ:{' '}
      <span
        className="level-badge"
        style={{
          color: LEVEL_COLORS[level] || '#333',
          borderColor: LEVEL_COLORS[level] || '#ddd',
        }}
      >
        {LEVEL_EMOJI[level]} {level}
      </span>
    </div>
  )
}
