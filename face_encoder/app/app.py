import os
from typing import Dict

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from database.crud import FaceEncoderCRUD
from utils.helpers.api_utils import send_request_to_face_encoding
from utils.helpers.session_utils import convert_bytes_to_megabytes, generate_unique_id
from utils.logger.logger import Logger
from utils.schema.face_encoder_schema import (
    FaceEncoderOutput,
    FaceEncoderSessionSummary,
)

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
async def start_session(user_id: str) -> Dict:
    """Start a new session and return the session ID"""
    try:
        session_id = generate_unique_id()
        logger.info(f"Starting session {session_id}")

        user_sessions = db_crud.get_user_oppened_sessions(user_id=user_id)
        logger.info(f"User {user_id} has {len(user_sessions)} sessions open")
        if len(user_sessions) > 0:
            logger.warning(f"User {user_id} has more than 1 session open")
            logger.info(f"Closing {user_id} previous session")
            db_crud.close_user_session(user_id=user_id)

        db_crud.add_user_session(session_id=session_id, user_id=user_id)

        return JSONResponse(content={"session_id": session_id}, status_code=200)
    except Exception as e:
        msg = f"Error while starting session: {str(e)}"
        logger.error(msg)
        return JSONResponse(content={"message": msg}, status_code=500)


@app.post("/upload")
async def upload(session_id: str, file: UploadFile = File(...)) -> JSONResponse:
    """Upload an image to the face-encoding service

    Args:
        file (UploadFile, optional): Selfie image to upload. Defaults to File(...).
        session_id (str): Session ID

    Returns:
        FaceEncoderOutput | None: Face Encoder Output Model
    """
    logger.debug("Uploading image")
    try:
        try:
            logger.debug("Checking if session exists")
            if not db_crud.check_if_session_exists(session_id):
                msg = f"Session {session_id} not found"
                logger.error(msg)
                return JSONResponse(content={"message": msg}, status_code=404)
        except ValueError as e:
            msg = f"Error while checking session existence: {str(e)}"
            logger.error(msg)
            return JSONResponse(content={"message": msg}, status_code=500)

        if file.size > MAX_FILE_SIZE:
            msg = f"The file is too large. \
                    File should be less than {convert_bytes_to_megabytes(MAX_FILE_SIZE)} MB. \
                    FileSize: {convert_bytes_to_megabytes(file.size)} MB"
            logger.error(msg)
            return JSONResponse(content={"message": msg}, status_code=400)

        if db_crud.get_session_count(session_id) >= 5:
            msg = "Session limit reached. Maximum of 5 files per session"
            logger.warning(msg)
            return JSONResponse(content={"message": msg}, status_code=400)

        contents = await file.read()

        _response = send_request_to_face_encoding(contents=contents)

        logger.debug("Image sent to the face-encoding service")

        if _response.status_code != 200:
            logger.error(
                (
                    "There was an error uploading the file to the face-encoding service."
                    "Status code: %s",
                    _response.status_code,
                )
            )
            return JSONResponse(
                content={"message": _response.text}, status_code=_response.status_code
            )

        logger.info(f"Session {session_id} uploaded image {file.filename}")
        db_crud.add_session(session_id=session_id, face_encodings=_response.json())

        response = FaceEncoderOutput(face_embedding=_response.json())

        return JSONResponse(content=response.model_dump(), status_code=200)

    except Exception as e:
        logger.exception(("There was an error uploading the file. Error: %s", e))
        return JSONResponse(content={"message": str(e)}, status_code=500)


@app.get("/session_summary/{session_id}")
async def session_summary(session_id: str) -> FaceEncoderSessionSummary:
    """Get the session summary

    Args:
        session_id (str): Session ID

    Returns:
        SessionSummary: Session Summary Model
    """
    try:
        logger.info(f"Getting session summary for session {session_id}")
        sess_summary = db_crud.get_session_summary(session_id=session_id)
    except ValueError as e:
        msg = (
            f"Failed to get session summary for session '{session_id}'. Error: {str(e)}"
        )
        logger.error(msg)
        return JSONResponse(content={"message": msg}, status_code=500)
    return sess_summary
