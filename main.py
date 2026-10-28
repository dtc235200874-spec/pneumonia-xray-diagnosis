from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("yolov8s-cls.pt")

    results = model.train(
        data=r"D:\DungVP\ViemPhoi\chest_xray",
        epochs=60,
        imgsz=224,
        device="cpu"  
    )