import os
import uuid
from fastapi import UploadFile, HTTPException
from src.inference import classify_image  # Your existing ML inference function

IMG_PATH = "data/test"  # Define image path constant


async def classify_and_save_image(file: UploadFile, gem_type: str):
    print("Uploaded File", file)
    print("Gem Type", gem_type)
    """Saves an uploaded image to disk and runs the classification model on it."""
    file_extension = os.path.splitext(file.filename)[1]
    if file_extension not in [".jpg", ".jpeg", ".png"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a JPG or PNG image.",
        )

    # Generate a unique filename to prevent overwrites
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(IMG_PATH, unique_filename)

    # Save the file to disk
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except IOError as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")

    # Run classification
    try:
        classification_result = classify_image(
            file_path
        )  # Assumes this returns a dict like {"State": "..."}
        if not classification_result:
            raise ValueError("Classification model returned an invalid result.")
    except Exception as e:
        # Catch potential errors from the ML model (e.g., file not found, processing error)
        # and raise a specific server error.
        raise HTTPException(
            status_code=500, detail=f"Error during model inference: {e}"
        )

    return {
        "result": classification_result.get("State", "Unknown"),
        "filename": unique_filename,
        "gemType": gem_type,
    }
