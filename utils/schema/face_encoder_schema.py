from datetime import datetime
from typing import List, Optional

from fastapi import UploadFile, File
from pydantic import BaseModel, Field


class FaceEncoderInput(BaseModel):
    """Face Encoder Input Model"""

    selfie_file: UploadFile = Field(title="Selfie file", default=File(...))


class FaceEncoderOutput(BaseModel):
    """Face Encoder Output Model"""

    face_embedding: List[List[float]] = Field(title="Face embedding")
    timestamp: str = Field(default_factory=lambda: str(datetime.now()))


class FaceEncoderSessionSummary(BaseModel):
    """Face Encoder Session Summary Model"""

    session_id: str = Field(title="Session ID")
    all_face_encodings: Optional[List[List]] = Field(
        title="List of all face Encodings", default_factory=list
    )
    created_at: str = Field(
        title="Timestamp of session creation", default_factory=datetime.now
    )
