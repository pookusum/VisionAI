import os
import json
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

    Return ONLY valid JSON.

    Use exactly this structure:

    {
        "caption": "A concise and meaningful caption",
        "description": "A detailed description of the image",
        "scene": "The overall environment or scene",
        "objects": [
            {
                "name": "object name",
                "description": "brief description of the object"
            }
        ],
        "activities": [
            "visible activity or action"
        ]
    }

    Requirements:

    - The caption should be concise.
    - The description should explain the image in detail.
    - List the important visible objects.
    - Explain the overall scene/environment.
    - List visible activities or actions.
    - Do not invent objects or activities that are not reasonably
      visible in the image.
    - If no activity is visible, return an empty array.
    - Return valid JSON only.
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
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

    text = response.text.strip()

    # Remove markdown code fences if Gemini adds them
    if text.startswith("```json"):
        text = text[7:]

    if text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    return json.loads(text)