from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# ========================
# SQLAlchemy ORM Models
# ========================

class UserPhoto(Base):
    __tablename__ = "user_photos"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow)
    face_shape = Column(String, nullable=True)

    # связь с рекомендациями
    recommendations = relationship("HairstyleRecommendation", back_populates="photo")


class HairstyleRecommendation(Base):
    __tablename__ = "hairstyle_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    photo_id = Column(Integer, ForeignKey("user_photos.id"))
    style_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    preview_url = Column(String, nullable=True)  # если храним превью на сервере
    created_at = Column(DateTime, default=datetime.utcnow)

    photo = relationship("UserPhoto", back_populates="recommendations")


class TryOnResult(Base):
    __tablename__ = "tryon_results"

    id = Column(Integer, primary_key=True, index=True)
    photo_id = Column(Integer, ForeignKey("user_photos.id"))
    style_id = Column(String, nullable=False)
    result_url = Column(String, nullable=False)  # ссылка на try-on фото
    created_at = Column(DateTime, default=datetime.utcnow)


# ========================
# Pydantic Models (FastAPI)
# ========================

class HairstyleRecommendationSchema(BaseModel):
    style_id: str
    name: str
    description: Optional[str] = None
    preview_url: Optional[str] = None

    class Config:
        orm_mode = True


class RecommendationResponse(BaseModel):
    photo_id: int
    face_shape: str
    recommendations: List[HairstyleRecommendationSchema]

    class Config:
        orm_mode = True


class TryOnResponseSchema(BaseModel):
    photo_id: int
    style_id: str
    result_url: str

    class Config:
        orm_mode = True
