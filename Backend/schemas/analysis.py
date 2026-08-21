from pydantic import BaseModel
from typing import List


class DetectedObject(BaseModel):
    name: str
    description: str


class ImageAnalysis(BaseModel):
    caption: str
    description: str
    scene: str
    objects: List[DetectedObject]
    activities: List[str]