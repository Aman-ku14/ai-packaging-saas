from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import uuid
from typing import List

router = APIRouter()

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    Uploads a product image.
    Validates file type (JPG/PNG) and size (<5MB).
    Returns the file ID and path.
    """
    
    # 1. Validate Extension
    filename = file.filename.lower()
    ext = filename.split(".")[-1] if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS or file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only JPG and PNG allowed."
        )

    # 2. Validate Size (Naive check - read into memory is safer for small files)
    # For strict stream handling, we'd read chunk by chunk.
    # Given 5MB limit, reading into memory/checking spooled file size is acceptable MVP.
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    
    if size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size is 5MB."
        )

    # 3. Save File
    file_id = str(uuid.uuid4())
    safe_filename = f"{file_id}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 4. AI Heuristics
    from app.ai.heuristics import analyze_image_fragility
    analysis = analyze_image_fragility(file_path)

    return {
        "file_id": file_id,
        "filename": safe_filename,
        "path": file_path,
        "message": "Image uploaded successfully",
        "suggested_fragility": analysis["suggested_fragility"],
        "confidence": analysis["confidence"],
        "analysis_note": analysis["reasoning"]
    }
