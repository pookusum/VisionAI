from fastapi import APIRouter, UploadFile, File, HTTPException

from services.gemini_service import analyze_image


router = APIRouter(
    prefix="/api",
    tags=["Image Analysis"]
)


@router.post("/analyze-image")
async def analyze_uploaded_image(
    image: UploadFile = File(...)
):

    # Check that a file was actually uploaded
    if not image:
        raise HTTPException(
            status_code=400,
            detail="No image uploaded."
        )

    # Supported image types
    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/webp"
    ]

    if image.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format. Please upload JPG, PNG, or WEBP."
        )

    try:

        # Read image bytes
        image_bytes = await image.read()

        # Make sure image is not empty
        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty."
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

        print("Gemini Error:", str(e))

        raise HTTPException(
            status_code=500,
            detail="Failed to analyze the image."
        )