from fastapi import FastAPI
from routers.predict import router as predict_router

app = FastAPI(title="Fraud Call Detection API")

app.include_router(predict_router, prefix="/predict")
