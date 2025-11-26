from fastapi import FastAPI
from app.routers import hairstyle
from app.database import Base, engine

# создаём таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Barbershop AI App")

app.include_router(hairstyle.router, prefix="/api/hairstyle")
