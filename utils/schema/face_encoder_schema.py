from datetime import datetime
from typing import List

from fastapi import UploadFile, File
from pydantic import BaseModel, Field


class FaceEncoderInput(BaseModel):
    """Face Encoder Input Model"""

    selfie_file: UploadFile = Field(title="Selfie file", default=File(...))


class FaceEncoderOutput(BaseModel):
    face_embedding: List[List[float]] = Field(title="Face embedding")
    timestamp: str = Field(default_factory=lambda: str(datetime.now()))
