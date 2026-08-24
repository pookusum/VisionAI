from fastapi import APIRouter, UploadFile, File, HTTPException

from services.gemini_service import analyze_image


router = APIRouter(
    prefix="/api",
    tags=["Image Analysis"]
)


MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

ALLOWED_TYPES = [
    "image/jpeg",
    "image/png",
    "image/webp"
]


@router.post("/analyze-image")
async def analyze_uploaded_image(
    image: UploadFile = File(...)
):

    if not image:
        raise HTTPException(
            status_code=400,
            detail="No image uploaded."
        )

    # Check file type
    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format. Please upload JPG, PNG, or WEBP."
        )

    try:
        image_bytes = await image.read()

        # Check empty file
        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty."
            )
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

        if len(image_bytes) > MAX_FILE_SIZE:
            raise HTTPException(
        status_code=400,
        detail="Image size must be less than 10 MB."
    )
        
        # Send image to Gemini
        result = analyze_image(
            image_bytes=image_bytes,
            mime_type=image.content_type
        )

        return {
            "success": True,
            "filename": image.filename,
            "analysis": result
        }

    except HTTPException:
        raise

    except Exception as e:

        print("Image analysis error:", repr(e))

        raise HTTPException(
            status_code=500,
            detail="Failed to analyze the image. Please try again."
    )