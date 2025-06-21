import os
import uuid
from fastapi import UploadFile
from src.inference import classify_image  # Your existing ML inference function

IMG_PATH = "data/test"  # Define image path constant


async def classify_and_save_image(file: UploadFile, gem_type: str):
    print("Uploaded File", file)
    print("Gem Type", gem_type)
    """Saves an uploaded image to disk and runs the classification model on it."""

    # Generate a unique filename to prevent overwrites
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(IMG_PATH, unique_filename)

    # Save the file to disk
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    # Run classification
    classification_result = classify_image(
        file_path
    )  # Assumes this returns a dict like {"State": "..."}

    return {
        "result": classification_result.get("State", "Unknown"),
        "filename": unique_filename,
        "gemType": gem_type,
    }
