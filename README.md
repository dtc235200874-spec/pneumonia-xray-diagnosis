# 🩺 Chẩn đoán viêm phổi (X-quang) — bản React

Trang web giao diện **React** (Vite) + backend **FastAPI** giữ nguyên mô hình YOLOv8
từ bản Gradio cũ (`app.py` — vẫn giữ nguyên để đối chiếu).

## Cấu trúc

```
ViemPhoi/
├── app.py                  # bản Gradio cũ (giữ nguyên, không sửa)
├── backend/
│   ├── main.py             # FastAPI: POST /api/predict + serve bản build React
│   └── requirements.txt
├── frontend/               # Vite + React (JavaScript)
│   └── src/
│       ├── App.jsx
│       ├── api.js
│       └── components/     # UploadZone, ResultPanel, ConfidenceChart
├── runs/                   # mô hình đã train (best.pt)
└── chest_xray/             # dữ liệu
```

## Yêu cầu

- Python 3.11+ (môi trường: `.venv` trong thư mục dự án)
- Node.js 18+

## Chạy development (2 tab_terminal)

```powershell
# Tab 1 — backend (cổng 8000)
cd D:\DungVP\ViemPhoi
.venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000

# Tab 2 — frontend (cổng 5173, tự proxy /api sang 8000)
cd D:\DungVP\ViemPhoi\frontend
npm run dev
# mở http://localhost:5173
```

## Chạy production (1 tiến trình duy nhất)

```powershell
cd D:\DungVP\ViemPhoi\frontend
npm run build
cd ..
.venv\Scripts\python.exe -m uvicorn backend.main:app --port 8000
# mở http://localhost:8000
```

## API

- `POST /api/predict` — multipart, field `file` (ảnh ≤ 10MB) → JSON:
  `{ label, confidence, level, is_pneumonia, probabilities, annotated_image }`
- `GET /api/health` — kiểm tra server và trạng thái mô hình

## So sánh với bản Gradio cũ

- Logic dự đoán, ngưỡng tin cậy (0.60 / 0.85), viền màu đỏ/xanh: **giữ nguyên**.
- Biểu đồ matplotlib được thay bằng biểu đồ recharts chạy ngay trên trình duyệt.
- Thêm kiểm tra loại file / kích thước ảnh và thông báo lỗi tiếng Việt.
