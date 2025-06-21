from fastapi import APIRouter, File, Form, UploadFile
from src.services import classify_service

router = APIRouter()


@router.post("/")
async def classify_image_endpoint(
    file: UploadFile = File(...),
    gemType: str = Form(...),
):
    """Receives an image and forwards it to the classification service."""
    result = await classify_service.classify_and_save_image(file, gemType)
    return result
