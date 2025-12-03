import requests
from fastapi import UploadFile, HTTPException

# URL твоего ML-сервиса
ML_SERVICE_URL = "http://ml-service:5100"  
# если локально:
# ML_SERVICE_URL = "http://127.0.0.1:5100"


def get_recommendations(image: UploadFile) -> dict:
    """
    Отправляет изображение в ML-сервис и получает рекомендации причесок
    """

    try:
        files = {
            "image": (image.filename, image.file, image.content_type)
        }

        response = requests.post(
            f"{ML_SERVICE_URL}/recommend",
            files=files,
            timeout=60
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"ML service error: {response.text}"
            )

        return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to ML service: {str(e)}"
        )


def do_tryon(image: UploadFile, style_id: str) -> bytes:
    """
    Отправляет фото + id прически в ML-сервис и получает изображение результата
    """

    try:
        files = {
            "image": (image.filename, image.file, image.content_type)
        }

        data = {
            "style_id": style_id
        }

        response = requests.post(
            f"{ML_SERVICE_URL}/tryon",
            files=files,
            data=data,
            timeout=120
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"ML try-on error: {response.text}"
            )

        return response.content  # ✅ тут возвращаем JPEG bytes

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to ML service: {str(e)}"
        )
