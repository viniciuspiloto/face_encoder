from typing import Dict
from sqlmodel import select

from database.database import FaceEncoderDB
from database.models import FaceEncoderSession, FaceEncoderSessionSummary
from utils.logger.logger import Logger

logger = Logger("face-encoder")


class FaceEncoderCRUD(FaceEncoderDB):
    """Face Encoder CRUD Class"""

    def add_session(
        self,
        session_id: str,
        face_encodings: Dict = None,
    ):
        """Add a session and face encodings to the database

        Args:
            session_id (str): The session ID to be added.
            face_encodings (Dict, optional): The face encodings to be added. Defaults to None.

        Raises:
            ValueError: Failed to add session to database
        """
        with self.get_session() as session:
            try:
                logger.info(f"Adding session {session_id} to database")
                session.add(
                    FaceEncoderSession(
                        session_id=session_id, face_encoding=face_encodings
                    )
                )
                session.commit()
            except Exception as e:
                raise ValueError(f"Failed to add session to database: {str(e)}") from e

    def get_session_count(self, session_id: str) -> int:
        """Get the number of sessions in the database

        Args:
            session_id (str): The session ID.

        Raises:
            ValueError: Failed to get session count from database

        Returns:
            int: The number of session entries in the database
        """
        with self.get_session() as session:
            try:
                statement = select(FaceEncoderSession).where(
                    FaceEncoderSession.session_id == session_id
                )
                results = session.exec(statement)
                session_obj = results.all()
                return len(session_obj)

            except Exception as e:
                raise ValueError(
                    f"Failed to get session count from database: {str(e)}"
                ) from e

    def get_session_summary(self, session_id: str) -> FaceEncoderSessionSummary:
        """Get the session summary from the database

        Args:
            session_id (str): The session ID.

        Raises:
            ValueError: Failed to get session summary from database

        Returns:
            FaceEncoderSessionSummary: The session summary
        """
        with self.get_session() as session:
            try:
                statement = select(FaceEncoderSession).where(
                    FaceEncoderSession.session_id == session_id,
                    FaceEncoderSession.face_encoding is not None,
                )
                results = session.exec(statement)
                session_obj = results.all()
                return FaceEncoderSessionSummary(
                    session_id=session_id,
                    all_face_encodings=[
                        session_obj[i].face_encoding for i in range(len(session_obj))
                    ],
                )
            except Exception as e:
                raise ValueError(
                    f"Failed to get session summary from database: {str(e)}"
                ) from e
