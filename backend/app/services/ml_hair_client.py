import requests
from fastapi import UploadFile

ML_HAIR_URL = "http://ml_hair:5100"  # адрес контейнера ML

def get_recommendations(image: UploadFile, top_k: int = 5):
    files = {"image": (image.filename, image.file, image.content_type)}
    data = {"top_k": str(top_k)}
    r = requests.post(f"{ML_HAIR_URL}/recommend", files=files, data=data)
    return r.json()

def do_tryon(image: UploadFile, style_id: str):
    files = {"image": (image.filename, image.file, image.content_type)}
    data = {"style_id": style_id}
    r = requests.post(f"{ML_HAIR_URL}/tryon", files=files, data=data)
    return r.content  # вернёт JPEG
