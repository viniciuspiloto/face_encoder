import requests


def build_api_url(endpoint: str, host: str = "localhost", port: int = 8000) -> str:
    """Build the API URL

    Args:
        endpoint (str): API endpoint
        host (str, optional): Host name. Defaults to "localhost".
        port (int, optional): Port. Defaults to 8000.

    Returns:
        str: API URL
    """
    return f"http://{host}:{port}/{endpoint}"


def send_request_to_face_encoding(
    endpoint: str = "v1/selfie",
    host: str = "face-encoding",
    port: int = 8000,
    contents: bytes = None,
    timeout: int = 60,
) -> requests.Response:
    """Send a request to the face-encoding service

    Args:
        endpoint (str, optional): Endpoint to send the request. Defaults to "v1/selfie".
        host (str, optional): Host name of the face-encoding service. Defaults to "face-encoding".
        port (int, optional): Port of the face-encoding service. Defaults to 8000.
        timeout (int, optional): Timeout of the request. Defaults to 60.

    Raises:
        requests.exceptions.RequestException: Error connecting to face-encoding service

    Returns:
        requests.Response: Response from the face-encoding service
    """
    try:
        return requests.post(
            build_api_url(endpoint, host, port),
            files={"file": contents},
            timeout=timeout,
        )
    except requests.exceptions.RequestException as e:
        error_message = f"Error connecting to face-encoding service: {str(e)}"
        raise requests.exceptions.RequestException(error_message) from e
