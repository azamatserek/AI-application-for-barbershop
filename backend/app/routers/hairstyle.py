from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database, ml_hair_client
import shutil
import uuid
import os
from fastapi.responses import FileResponse

router = APIRouter()

UPLOAD_FOLDER = "./uploaded_photos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Рекомендации ---
@router.post("/recommend", response_model=models.RecommendationResponse)
async def recommend(image: UploadFile = File(...), db: Session = Depends(database.get_db)):
    # сохраняем фото на сервер
    photo_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_FOLDER, f"{photo_id}.jpg")
    with open(file_path, "wb") as f:
        shutil.copyfileobj(image.file, f)

    # вызываем ML сервис
    ml_result = ml_hair_client.get_recommendations(image)

    # сохраняем в БД
    user_photo = models.UserPhoto(filename=f"{photo_id}.jpg", content_type=image.content_type)
    db.add(user_photo)
    db.commit()
    db.refresh(user_photo)

    # сохраняем рекомендации
    for rec in ml_result["recommendations"]:
        recommendation = models.HairstyleRecommendation(
            photo_id=user_photo.id,
            style_id=rec["style_id"],
            name=rec["name"],
            description=rec.get("description"),
            preview_url=rec.get("preview_url")
        )
        db.add(recommendation)
    db.commit()

    return models.RecommendationResponse(
        photo_id=user_photo.id,
        face_shape=ml_result.get("face_shape", "unknown"),
        recommendations=[models.HairstyleRecommendationSchema(**r) for r in ml_result["recommendations"]]
    )


# --- Try-On ---
@router.post("/tryon")
async def tryon(style_id: str, image: UploadFile = File(...)):
    result_bytes = ml_hair_client.do_tryon(image, style_id)
    file_name = f"{uuid.uuid4()}.jpg"
    result_path = os.path.join(UPLOAD_FOLDER, file_name)
    with open(result_path, "wb") as f:
        f.write(result_bytes)
    return FileResponse(result_path, media_type="image/jpeg")
