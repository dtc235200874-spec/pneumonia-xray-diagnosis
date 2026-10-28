import cv2
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO
import gradio as gr

# ================= LOAD MODEL =================
model_path = r"D:\DungVP\ViemPhoi\runs\classify\train\weights\best.pt"
model = YOLO(model_path)

# ================= HÀM DỰ ĐOÁN =================
def predict(image):

    # ================= KIỂM TRA ẢNH =================
    if image is None:
        return (
            None,
            None,
            "<div class='result-box'>Vui lòng chọn ảnh</div>",
            None
        )

    # ================= CHUYỂN ẢNH =================
    img = np.array(image)

    # grayscale -> RGB
    if len(img.shape) == 2 or (
        len(img.shape) == 3 and img.shape[2] == 1
    ):
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    # ================= DỰ ĐOÁN =================
    results = model.predict(
        img,
        save=False,
        verbose=False
    )

    pred = results[0]

    # ================= LẤY KẾT QUẢ =================
    cls_id = int(pred.probs.top1)

    conf = float(pred.probs.top1conf)

    class_name = pred.names[cls_id]

    # ================= COPY ẢNH =================
    output_img = img.copy()

    # ================= MỨC ĐỘ =================
    if conf < 0.60:
        level = "🟡 Thấp"

    elif conf < 0.85:
        level = "🟠 Trung bình"

    else:
        level = "🔴 Cao"

    # ================= KẾT QUẢ =================
    if class_name.upper() == "PNEUMONIA":

        border_color = (255, 0, 0)

        result_text = f"""
        <div class='result-box red'>

            🔴 VIÊM PHỔI <br><br>

            Độ tin cậy: <b>{conf:.2f}</b><br><br>

            Mức độ: <b>{level}</b>

        </div>
        """

    else:

        border_color = (0, 255, 0)

        result_text = f"""
        <div class='result-box green'>

            ✅ BÌNH THƯỜNG <br><br>

            Độ tin cậy: <b>{conf:.2f}</b><br><br>

            Mức độ: <b>{level}</b>

        </div>
        """

    # ================= VẼ KHUNG =================
    cv2.rectangle(
        output_img,
        (5, 5),
        (output_img.shape[1] - 5,
         output_img.shape[0] - 5),
        border_color,
        10
    )

    # ================= BIỂU ĐỒ =================
    probs = pred.probs.data.cpu().numpy()

    labels = list(pred.names.values())

    fig, ax = plt.subplots(figsize=(5, 4))

    ax.bar(labels, probs)

    ax.set_ylim(0, 1)

    ax.set_title("Confidence Score")

    plt.tight_layout()

    return (
        img,
        output_img,
        result_text,
        fig
    )

# ================= CSS =================
css = """
body{
    font-family:Arial;
}

/* TITLE */
#title{
    text-align:center;
    font-size:34px;
    font-weight:bold;
    margin-bottom:5px;
}

#subtitle{
    text-align:center;
    color:gray;
    margin-bottom:20px;
}

/* RESULT BOX */
.result-box{
    padding:20px;
    border-radius:12px;
    text-align:center;
    font-size:22px;
    font-weight:bold;
    margin-top:10px;
}

/* RED */
.red{
    background:#ffecec;
    color:red;
}

/* GREEN */
.green{
    background:#ecffec;
    color:green;
}
"""

# ================= GIAO DIỆN =================
with gr.Blocks(css=css) as app:

    # ================= HEADER =================
    gr.Markdown(
        "<div id='title'>🩺 CHẨN ĐOÁN VIÊM PHỔI (X-quang)</div>"
    )

    # ================= 2 ẢNH =================
    with gr.Row():

        image_input = gr.Image(
            label="Ảnh đầu vào",
            height=400
        )

        image_output = gr.Image(
            label="Kết quả",
            height=400
        )

    # ================= KẾT QUẢ =================
    result_text = gr.HTML(
        "<div class='result-box'>Kết quả sẽ hiển thị ở đây</div>"
    )

    # ================= BIỂU ĐỒ =================
    gr.Markdown("### 📊 Độ tin cậy mô hình")

    chart = gr.Plot()

    # ================= BUTTON =================
    with gr.Row():

        btn_predict = gr.Button(
            "🚀 Dự đoán",
            variant="primary"
        )

        btn_clear = gr.Button(
            "🧹 Xóa và làm lại"
        )

    # ================= CLICK DỰ ĐOÁN =================
    btn_predict.click(
        fn=predict,
        inputs=image_input,
        outputs=[
            image_input,
            image_output,
            result_text,
            chart
        ]
    )

    # ================= RESET =================
    btn_clear.click(
        fn=lambda: (
            None,
            None,
            "<div class='result-box'>Kết quả sẽ hiển thị ở đây</div>",
            None
        ),
        outputs=[
            image_input,
            image_output,
            result_text,
            chart
        ]
    )

# ================= CHẠY APP =================
if __name__ == "__main__":
    app.launch()