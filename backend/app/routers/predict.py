from fastapi import APIRouter
import requests
import os

router = APIRouter()

ML_URL = os.getenv("ML_SERVICE_URL")

@router.post("/")
def detect_fraud(data: dict):
    response = requests.post(f"{ML_URL}/infer", json=data)
    return response.json()
