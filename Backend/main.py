from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.image import router as image_router


app = FastAPI(
    title="VisionAI",
    description="AI-powered image captioning and visual understanding API",
    version="1.0.0"
)


# Allow requests from our Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:3000",
    "http://127.0.0.1:3000"
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routes
app.include_router(image_router)


@app.get("/")
def root():
    return {
        "message": "VisionAI API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }