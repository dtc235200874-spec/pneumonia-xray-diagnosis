export async function predictImage(file) {
  const form = new FormData()
  form.append('file', file)

  let res
  try {
    res = await fetch('/api/predict', { method: 'POST', body: form })
  } catch {
    throw new Error('Không kết nối được máy chủ. Hãy chắc chắn backend đang chạy (uvicorn trên cổng 8000).')
  }

  if (!res.ok) {
    let detail = 'Có lỗi xảy ra khi phân tích ảnh.'
    try {
      const body = await res.json()
      if (body && body.detail) detail = body.detail
    } catch {
      /* giữ thông báo mặc định */
    }
    throw new Error(detail)
  }

  return res.json()
}
