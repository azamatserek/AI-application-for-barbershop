import os
from random import sample

HAIRSTYLE_DIR = "./hairstyles"

def recommend_hairstyles(image_bytes, k=3):
    """
    Заглушка для рекомендаций.
    Возвращает k случайных причесок из папки hairstyles
    """
    styles = os.listdir(HAIRSTYLE_DIR)
    selected = sample(styles, min(k, len(styles)))

    recommendations = []
    for s in selected:
        recommendations.append({
            "style_id": s.split('.')[0],
            "name": s.split('.')[0].capitalize(),
            "preview_url": f"/hairstyles/{s}"
        })

    # Для MVP можно жестко вернуть форму лица
    return {"face_shape": "oval", "recommendations": recommendations}
