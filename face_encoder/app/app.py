import os
from typing import Dict
from fastapi import FastAPI, File, UploadFile
import requests

from database.crud import FaceEncoderCRUD

# from database.models import SessionSummary
from utils.helpers.session_utils import convert_bytes_to_megabytes, generate_unique_id
from utils.logger.logger import Logger
from utils.schema.face_encoder_schema import FaceEncoderOutput

app = FastAPI(title="Face Encoder")

logger = Logger("face-encoder")
db_crud = FaceEncoderCRUD()
db_crud.drop_db_and_tables()
db_crud.create_db_and_tables()

MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "2000000"))


@app.get("/ping")
async def ping() -> Dict:
    """Pings the service

    Returns:
        Dict: Status of the service
    """
    return {"status": 200}


@app.post("/start_session")
async def start_session():
    """Start a new session and return the session ID"""
    session_id = generate_unique_id()
    logger.info(f"Starting session {session_id}")

    return {"session_id": session_id}


@app.post("/upload")
async def upload(
    session_id: str, file: UploadFile = File(...)
) -> FaceEncoderOutput | None:
    """Upload an image to the face-encoding service

    Args:
        file (UploadFile, optional): Selfie image to upload. Defaults to File(...).
        session_id (str): Session ID

    Returns:
        FaceEncoderOutput | None: Face Encoder Output Model
    """
    logger.debug("Uploading image")
    try:
        if file.size > MAX_FILE_SIZE:
            msg = f"The file is too large. \
                    File should be less than {convert_bytes_to_megabytes(MAX_FILE_SIZE)} MB. \
                    FileSize: {convert_bytes_to_megabytes(file.size)} MB"
            logger.error(msg)
            return {"message": msg}

        if db_crud.get_session_count(session_id) >= 5:
            msg = "Session limit reached. Maximum of 5 sessions per user"
            logger.warning(msg)
            return {"message": msg}

        contents = await file.read()

        _response = requests.post(
            "http://face-encoding:8000/v1/selfie", files={"file": contents}, timeout=60
        )
        logger.debug("Image sent to the face-encoding service")

        if _response.status_code != 200:
            logger.error(
                (
                    "There was an error uploading the file to the face-encoding service."
                    "Status code: %s",
                    _response.status_code,
                )
            )

        logger.info(f"Session {session_id} uploaded image {file.filename}")
        db_crud.add_session(session_id=session_id, face_encodings=_response.json())

        response = FaceEncoderOutput(face_embedding=_response.json())

        return response

    except Exception as e:
        logger.exception(("There was an error uploading the file. Error: %s", e))
        return {"message": str(e)}


@app.get("/session_summary/{session_id}")
async def session_summary(session_id: str):
    """Get the session summary

    Args:
        session_id (str): Session ID

    Returns:
        SessionSummary: Session Summary Model
    """
    logger.info(f"Getting session summary for session {session_id}")
    sess_summary = db_crud.get_session_summary(session_id=session_id)
    return sess_summary
