import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")

client = genai.Client(api_key=API_KEY)


def analyze_image(image_bytes: bytes, mime_type: str):
    prompt = """
    Analyze this image carefully.

    Provide:

    1. A concise and meaningful caption.
    2. A detailed description of the image.
    3. The main objects visible in the image.
    4. The overall scene or environment.
    5. Any visible activities or actions.

    Do not invent objects or details that are not reasonably
    visible in the image.

    Return the result in a clear and structured format.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            {
                "inline_data": {
                    "mime_type": mime_type,
                    "data": image_bytes,
                }
            },
            prompt,
        ],
    )

    return response.text