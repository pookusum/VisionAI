import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")


# Create Gemini client
client = genai.Client(api_key=API_KEY)


def analyze_image(image_bytes: bytes, mime_type: str):

    prompt = """
Analyze the provided image carefully.

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

Rules:

- The caption must be concise.
- The description should describe the image accurately.
- Identify important visible objects.
- Describe the overall scene/environment.
- List visible activities or actions.
- Do not invent objects.
- Do not invent activities.
- If there are no visible activities, return an empty array.
- Return JSON only.
"""

    try:

        # Convert uploaded image bytes into a Gemini image Part
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type
        )

        # Send image + prompt to Gemini
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                image_part,
                prompt
            ],
        )

        # Get Gemini's text response
        text = response.text.strip()

        # Remove markdown code fences if Gemini adds them
        if text.startswith("```json"):
            text = text[7:]

        elif text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        # Convert JSON string into Python dictionary
        result = json.loads(text)

        return result

    except Exception as e:
        print("Gemini service error:", repr(e))
        raise