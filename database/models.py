from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel
from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class FaceEncoderSession(SQLModel, table=True):
    """Face Encoder Session Model"""

    __tablename__ = "sessions"
    id: int | None = Field(title="ID", default=None, primary_key=True)
    session_id: str = Field(title="Session ID", index=True)
    face_encoding: Optional[Dict] = Field(
        title="Face Encoding", default_factory=dict, sa_column=Column(JSON)
    )
    created_at: datetime = Field(
        title="Timestamp of session creation", default_factory=datetime.now()
    )

    class Config:
        """Class configuration"""

        arbitrary_types_allowed = True


class FaceEncoderUserSessions(SQLModel, table=True):
    """Face Encoder User Sessions Model"""

    __tablename__ = "user_sessions"
    session_id: str = Field(title="Session ID", primary_key=True)
    user_id: str = Field(title="User ID", index=True)
    created_at: datetime = Field(
        title="Timestamp of session creation", default_factory=datetime.now()
    )
    closed_at: Optional[datetime] = Field(
        title="Timestamp of session close", default=None
    )


class FaceEncoderSessionSummary(BaseModel):
    """Face Encoder Session Summary Model"""

    session_id: str = Field(title="Session ID")
    all_face_encodings: Optional[List[List]] = Field(
        title="List of all face Encodings", default_factory=list
    )
