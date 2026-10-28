"""Backend FastAPI cho trang chẩn đoán viêm phổi (bản React).

Tái sử dụng nguyên logic dự đoán từ app.py (Gradio):
giữ mô hình YOLOv8-cls best.pt, ngưỡng tin cậy 0.60/0.85,
khung viền đỏ/xanh quanh ảnh kết quả.
"""

import base64
import sys
import threading
from contextlib import asynccontextmanager
from pathlib import Path

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "runs" / "classify" / "train" / "weights" / "best.pt"
DIST_DIR = BASE_DIR / "frontend" / "dist"

MAX_UPLOAD_BYTES = 10 * 1024 * 1024

model = None
predict_lock = threading.Lock()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Tai mo hinh dung mot lan khi khoi dong server."""
    global model
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Khong tim thay file mo hinh: {MODEL_PATH}. "
            "Hay kiem tra thu muc runs/classify/train/weights."
        )
    model = YOLO(str(MODEL_PATH))
    print(f"Da tai mo hinh: {MODEL_PATH}")
    yield


app = FastAPI(title="API chẩn đoán viêm phổi", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def to_display_rgb(img: np.ndarray) -> np.ndarray:
    """Chuyen anh grayscale/RGBA sang RGB (giong app.py goc)."""
    if img.ndim == 2:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    if img.ndim == 3 and img.shape[2] == 1:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    if img.ndim == 3 and img.shape[2] == 4:
        return cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    return img


@app.get("/api/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/api/predict")
def predict(file: UploadFile = File(...)):
    raw = file.file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="File rỗng. Vui lòng chọn một ảnh X-quang.")
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=400, detail="Ảnh quá lớn. Tối đa 10MB.")

    img = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_UNCHANGED)
    if img is None:
        raise HTTPException(
            status_code=400,
            detail="Không đọc được ảnh. Vui lòng chọn file JPG/PNG hợp lệ.",
        )
    img = to_display_rgb(img)

    with predict_lock:
        pred = model.predict(img, save=False, verbose=False)[0]

    cls_id = int(pred.probs.top1)
    conf = float(pred.probs.top1conf)
    class_name = str(pred.names[cls_id]).upper()

    # Muc do tin cậy — giong nguong cua app.py goc
    if conf < 0.60:
        level = "Thấp"
    elif conf < 0.85:
        level = "Trung bình"
    else:
        level = "Cao"

    # Ve khung vien ket qua
    output_img = img.copy()
    is_pneumonia = class_name == "PNEUMONIA"
    border_color = (255, 0, 0) if is_pneumonia else (0, 255, 0)
    cv2.rectangle(
        output_img,
        (5, 5),
        (output_img.shape[1] - 5, output_img.shape[0] - 5),
        border_color,
        10,
    )

    probs = pred.probs.data.cpu().numpy()
    probabilities = [
        {"name": str(pred.names[i]), "prob": round(float(p), 4)}
        for i, p in enumerate(probs)
    ]

    ok, buf = cv2.imencode(".png", cv2.cvtColor(output_img, cv2.COLOR_RGB2BGR))
    if not ok:
        raise HTTPException(status_code=500, detail="Không mã hóa được ảnh kết quả.")
    annotated_b64 = base64.b64encode(buf.tobytes()).decode("ascii")

    return {
        "label": class_name,
        "confidence": round(conf, 4),
        "level": level,
        "is_pneumonia": is_pneumonia,
        "probabilities": probabilities,
        "annotated_image": f"data:image/png;base64,{annotated_b64}",
    }


# Phuc vu ban build React (frontend/dist) neu da co — che do production chi can uvicorn.
if DIST_DIR.exists():
    from fastapi.staticfiles import StaticFiles

    app.mount("/", StaticFiles(directory=str(DIST_DIR), html=True), name="frontend")
