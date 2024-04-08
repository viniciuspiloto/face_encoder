from datetime import datetime
from typing import Dict, List

from sqlalchemy.sql.operators import is_
from sqlmodel import select, update

from database.database import FaceEncoderDB
from database.models import FaceEncoderSession, FaceEncoderUserSessions
from utils.logger.logger import Logger
from utils.schema.face_encoder_schema import FaceEncoderSessionSummary

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

                if len(session_obj) == 0:
                    msg = f"Session {session_id} not found"
                    logger.error(msg)
                    raise ValueError(msg)

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

    def add_user_session(self, session_id: str, user_id: str):
        """Add a user session to the database

        Args:
            session_id (str): The session ID to be added.
            user_id (str): The user ID to be added.

        Raises:
            ValueError: Failed to add user session to database
        """
        with self.get_session() as session:
            try:
                logger.info(f"Adding user session {session_id} to database")
                session.add(
                    FaceEncoderUserSessions(session_id=session_id, user_id=user_id)
                )
                session.commit()
            except Exception as e:
                raise ValueError(
                    f"Failed to add user session to database: {str(e)}"
                ) from e

    def get_user_session(self, user_id: str) -> List[FaceEncoderUserSessions]:
        """Get the user sessions from the database

        Args:
            user_id (str): The user ID.

        Raises:
            ValueError: Failed to get user sessions from database

        Returns:
            List[FaceEncoderUserSessions]: The user sessions
        """
        with self.get_session() as session:
            try:
                statement = select(FaceEncoderUserSessions).where(
                    FaceEncoderUserSessions.user_id == user_id
                )
                results = session.exec(statement)
                return results.all()
            except Exception as e:
                raise ValueError(
                    f"Failed to get user sessions from database: {str(e)}"
                ) from e

    def check_if_session_exists(self, session_id: str) -> bool:
        """Check if the session exists in the database

        Args:
            session_id (str): The session ID.

        Raises:
            ValueError: Failed to check if session exists in database

        Returns:
            bool: True if the session exists, False otherwise
        """
        with self.get_session() as session:
            try:
                statement = select(FaceEncoderUserSessions).where(
                    FaceEncoderUserSessions.session_id == session_id
                )
                results = session.exec(statement)
                return len(results.all()) > 0
            except Exception as e:
                raise ValueError(
                    f"Failed to check if session exists in database: {str(e)}"
                ) from e

    def close_user_session(self, user_id: str):
        """Close the user session in the database

        Args:
            user_id (str): The user ID.

        Raises:
            ValueError: Failed to close user session in database
        """
        with self.get_session() as session:
            try:
                logger.info(f"Closing user session {user_id} in database")
                statement = (
                    update(FaceEncoderUserSessions)
                    .where(FaceEncoderUserSessions.user_id == user_id)
                    .values(closed_at=datetime.now())
                )
                session.exec(statement)
                session.commit()
            except Exception as e:
                raise ValueError(
                    f"Failed to close user session in database: {str(e)}"
                ) from e

    def get_user_oppened_sessions(self, user_id: str) -> List[FaceEncoderUserSessions]:
        """Get the user opened sessions from the database

        Args:
            user_id (str): The user ID.

        Raises:
            ValueError: Failed to get user sessions from database

        Returns:
            List[FaceEncoderUserSessions]: The user sessions
        """
        with self.get_session() as session:
            try:
                statement = select(FaceEncoderUserSessions).where(
                    FaceEncoderUserSessions.user_id == user_id,
                    is_(FaceEncoderUserSessions.closed_at, None),
                )
                results = session.exec(statement)
                return results.all()
            except Exception as e:
                raise ValueError(
                    f"Failed to get user sessions from database: {str(e)}"
                ) from e
