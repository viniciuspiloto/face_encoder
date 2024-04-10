from typing import Any
from unittest.mock import patch

import pytest

from database.models import FaceEncoderUserSessions
from utils.schema.face_encoder_schema import FaceEncoderSessionSummary


@pytest.fixture(name="mock_face_encoder_crud")
def fixture_face_encoder_crud() -> Any:
    """Fixture for creating a mock FaceEncoderCRUD instance."""
    with patch("database.crud.FaceEncoderCRUD") as mock_cls:
        yield mock_cls.return_value


def test_add_session(mock_face_encoder_crud: Any) -> None:
    """Test the add_session method of the FaceEncoderCRUD class.

    Args:
        mock_face_encoder_crud (Any): Mocked FaceEncoderCRUD instance.
    """
    session_id = "e1353715-e74c-413f-83bc-8210ce61ad27"
    face_encodings = {"face_encodings": [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]]}

    mock_face_encoder_crud.add_session.return_value = None
    result = mock_face_encoder_crud.add_session(session_id, face_encodings)

    assert mock_face_encoder_crud.add_session.call_count == 1
    assert mock_face_encoder_crud.add_session.call_args[0][0] == session_id
    assert mock_face_encoder_crud.add_session.call_args[0][1] == face_encodings
    assert result is None


def test_get_session_count(mock_face_encoder_crud: Any) -> None:
    """Test the get_session_count method of the FaceEncoderCRUD class.

    Args:
        mock_face_encoder_crud (Any): Mocked FaceEncoderCRUD instance.
    """
    session_id = "e1353715-e74c-413f-83bc-8210ce61ad27"

    mock_face_encoder_crud.get_session_count.return_value = 5
    result = mock_face_encoder_crud.get_session_count(session_id)

    assert mock_face_encoder_crud.get_session_count.call_count == 1
    assert mock_face_encoder_crud.get_session_count.call_args[0][0] == session_id
    assert isinstance(result, int)
    assert result == 5


def test_get_session_summary(mock_face_encoder_crud: Any) -> None:
    """Test the get_session_summary method of the FaceEncoderCRUD class.

    Args:
        mock_face_encoder_crud (Any): Mocked FaceEncoderCRUD instance.
    """
    session_id = "e1353715-e74c-413f-83bc-8210ce61ad27"

    mock_face_encoder_crud.get_session_summary.return_value = FaceEncoderSessionSummary(
        session_id=session_id, face_encodings=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    )
    result = mock_face_encoder_crud.get_session_summary(session_id)

    assert mock_face_encoder_crud.get_session_summary.call_count == 1
    assert mock_face_encoder_crud.get_session_summary.call_args[0][0] == session_id
    assert mock_face_encoder_crud.get_session_summary.return_value is not None
    assert result == mock_face_encoder_crud.get_session_summary.return_value
    assert isinstance(result, FaceEncoderSessionSummary)


def test_add_user_session(mock_face_encoder_crud: Any) -> None:
    """Test the add_user_session method of the FaceEncoderCRUD class.

    Args:
        mock_face_encoder_crud (Any): Mocked FaceEncoderCRUD instance.
    """
    session_id = "e1353715-e74c-413f-83bc-8210ce61ad27"
    user_id = "36e9dbd1-6d33-48da-a7f8-9967b37b0644"

    mock_face_encoder_crud.add_user_session.return_value = None
    result = mock_face_encoder_crud.add_user_session(session_id, user_id)

    assert mock_face_encoder_crud.add_user_session.call_count == 1
    assert mock_face_encoder_crud.add_user_session.call_args[0][0] == session_id
    assert result is None


def test_get_user_session(mock_face_encoder_crud: Any) -> None:
    """Test the get_user_session method of the FaceEncoderCRUD class.

    Args:
        mock_face_encoder_crud (Any): Mocked FaceEncoderCRUD instance.
    """
    session_id = "e1353715-e74c-413f-83bc-8210ce61ad27"
    user_id = "36e9dbd1-6d33-48da-a7f8-9967b37b0644"
    user_sessions = [
        FaceEncoderUserSessions(
            session_id=session_id,
            face_encodings=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
        ),
        FaceEncoderUserSessions(
            session_id=session_id,
            face_encodings=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
        ),
    ]

    mock_face_encoder_crud.get_user_session.return_value = user_sessions
    result = mock_face_encoder_crud.get_user_session(session_id, user_id)

    assert mock_face_encoder_crud.get_user_session.call_count == 1
    assert mock_face_encoder_crud.get_user_session.call_args[0][0] == session_id
    assert isinstance(result, list)


def test_check_if_session_exists(mock_face_encoder_crud: Any) -> None:
    """Test the check_if_session_exists method of the FaceEncoderCRUD class.

    Args:
        mock_face_encoder_crud (Any): Mocked FaceEncoderCRUD instance.
    """
    session_id = "e1353715-e74c-413f-83bc-8210ce61ad27"

    mock_face_encoder_crud.check_if_session_exists.return_value = True
    result = mock_face_encoder_crud.check_if_session_exists(session_id)

    assert mock_face_encoder_crud.check_if_session_exists.call_count == 1
    assert mock_face_encoder_crud.check_if_session_exists.call_args[0][0] == session_id
    assert result is True


def test_close_user_session(mock_face_encoder_crud: Any) -> None:
    """Test the close_user_session method of the FaceEncoderCRUD class.

    Args:
        mock_face_encoder_crud (Any): Mocked FaceEncoderCRUD instance.
    """
    user_id = "36e9dbd1-6d33-48da-a7f8-9967b37b0644"

    mock_face_encoder_crud.close_user_session.return_value = None
    result = mock_face_encoder_crud.close_user_session(user_id)

    assert mock_face_encoder_crud.close_user_session.call_count == 1
    assert mock_face_encoder_crud.close_user_session.call_args[0][0] == user_id
    assert result is None


def test_get_user_oppened_sessions(mock_face_encoder_crud: Any) -> None:
    """Test the get_user_oppened_sessions method of the FaceEncoderCRUD class.

    Args:
        mock_face_encoder_crud (Any): Mocked FaceEncoderCRUD instance.
    """
    session_id = "e1353715-e74c-413f-83bc-8210ce61ad27"
    user_id = "36e9dbd1-6d33-48da-a7f8-9967b37b0644"
    user_sessions = [
        FaceEncoderUserSessions(
            session_id=session_id,
            face_encodings=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
        ),
        FaceEncoderUserSessions(
            session_id=session_id,
            face_encodings=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
        ),
    ]

    mock_face_encoder_crud.get_user_oppened_sessions.return_value = user_sessions
    result = mock_face_encoder_crud.get_user_oppened_sessions(user_id)

    assert mock_face_encoder_crud.get_user_oppened_sessions.call_count == 1
    assert mock_face_encoder_crud.get_user_oppened_sessions.call_args[0][0] == user_id
    assert isinstance(result, list)
