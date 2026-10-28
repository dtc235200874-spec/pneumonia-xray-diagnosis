from ultralytics import YOLO

# Load model đã train xong
model_path = r"D:\ViemPhoi\runs\classify\train\weights\best.pt"
model = YOLO(model_path)

# Đánh giá trên tập val/test
results = model.val(data=r"D:\VIEMPHOI\chest_xray")  

# In kết quả chính
print("📊 Kết quả đánh giá:")
print(f"Top-1 Accuracy : {results.top1:.4f}")
print(f"Top-5 Accuracy : {results.top5:.4f}")
print(f"Loss           : {results.loss:.4f}")
