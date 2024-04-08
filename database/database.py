from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

from database.config import FaceEncoderDBConfig
from utils.logger.logger import Logger

db_config = FaceEncoderDBConfig()

logger = Logger("face-encoder")


class FaceEncoderDB:
    """Face Encoder Database Class"""

    def __init__(self) -> None:
        logger.info("Creating database engine")
        self.engine = create_engine(db_config.get_url(), echo=True)

    def create_db_and_tables(self) -> None:
        """Creates the database and tables"""
        logger.info("Creating database and tables")
        SQLModel.metadata.create_all(self.engine, checkfirst=True)

    def drop_db_and_tables(self) -> None:
        """Drop the database and tables"""
        logger.info("Dropping database and tables")
        SQLModel.metadata.drop_all(self.engine)

    @contextmanager
    def get_session(self):
        """Get a session

        Yields:
            Session: Session object
        """
        with Session(self.engine) as session:
            yield session
