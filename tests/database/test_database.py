import pytest
from sqlalchemy import Engine

from database.database import FaceEncoderDB


@pytest.fixture(name="face_encoder_db")
def fixture_face_encoder_db():
    """Fixture for creating a mock FaceEncoderDB instance."""
    return FaceEncoderDB()


def test_face_encoder_db_initialization(face_encoder_db: FaceEncoderDB):
    """Test the initialization of the FaceEncoderDB class

    Args:
        face_encoder_db (FaceEncoderDB): An instance of the FaceEncoderDB class
    """
    assert isinstance(face_encoder_db, FaceEncoderDB)
    assert isinstance(face_encoder_db.engine, Engine)


def test_get_session(face_encoder_db: FaceEncoderDB):
    """Test the get_session method of the FaceEncoderDB class

    Args:
        face_encoder_db (FaceEncoderDB): An instance of the FaceEncoderDB class
    """
    with face_encoder_db.get_session() as session:
        assert session is not None
