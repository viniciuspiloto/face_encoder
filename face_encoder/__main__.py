import uvicorn

from utils.logger.logger import Logger

logger = Logger("face-encoder")


def main() -> None:
    """
    Run the application with specified logging and mode settings.
    """

    logger.info("Starting face encoder system")
    uvicorn.run(
        "face_encoder.app.app:app",
        port=8000,
        reload=True,
        host="0.0.0.0",
        log_config=None,
    )


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
