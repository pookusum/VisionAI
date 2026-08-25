from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from services.gemini_service import analyze_image


app = FastAPI(
    title="VisionAI",
    version="1.0.0",
    description="AI-powered image captioning and visual understanding API"
)


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://visionai-2.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "VisionAI API is running"
    }


@app.post("/api/analyze-image")
async def analyze_uploaded_image(
    image: UploadFile = File(...)
):

    try:
        image_bytes = await image.read()

        mime_type = image.content_type

        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/webp"
        ]

        if mime_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Only JPG, PNG and WEBP images are supported."
            )

        analysis = analyze_image(
            image_bytes=image_bytes,
            mime_type=mime_type
        )

        return {
            "success": True,
            "filename": image.filename,
            "analysis": analysis
        }

    except HTTPException:
        raise

    except Exception as e:

        print("API ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze image: {str(e)}"
        )