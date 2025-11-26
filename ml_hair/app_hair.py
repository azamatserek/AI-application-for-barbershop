from flask import Flask, request, send_file
from recommender import recommend_hairstyles
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)

# Папка для try-on результатов
RESULTS_DIR = "./results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# -----------------------
# Рекомендации причесок
# -----------------------
@app.route("/recommend", methods=["POST"])
def recommend():
    if "image" not in request.files:
        return {"error": "No image uploaded"}, 400
    image_file = request.files["image"]
    image_bytes = image_file.read()
    top_k = int(request.form.get("top_k", 3))

    recommendations = recommend_hairstyles(image_bytes, k=top_k)
    return recommendations

# -----------------------
# Try-On
# -----------------------
@app.route("/tryon", methods=["POST"])
def tryon():
    if "image" not in request.files or "style_id" not in request.form:
        return {"error": "Missing image or style_id"}, 400

    image_file = request.files["image"]
    style_id = request.form["style_id"]

    img = Image.open(image_file)

    # ----------------------
    # Место для настоящей модели U-Net
    # Пока заглушка: просто накладываем выбранную прическу сверху
    # ----------------------
    hairstyle_path = os.path.join("./hairstyles", f"{style_id}.jpg")
    if os.path.exists(hairstyle_path):
        hair = Image.open(hairstyle_path).resize(img.size)
        img.paste(hair, (0,0), hair if hair.mode=='RGBA' else None)

    result_path = os.path.join(RESULTS_DIR, f"{style_id}_{image_file.filename}")
    img.save(result_path)

    return send_file(result_path, mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100)
