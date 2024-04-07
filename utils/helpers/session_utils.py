import time
import uuid
import hashlib


def generate_unique_id():
    """
    A function to generate a unique ID using timestamp, random string, and hashlib.
    No parameters.
    Returns a string representing the ID.
    """
    timestamp = str(time.time())
    random_str = str(uuid.uuid4())
    unique_id = hashlib.md5((timestamp + random_str).encode()).hexdigest()

    return unique_id


def convert_bytes_to_megabytes(size_in_bytes: int, decimal_places: int = 2) -> float:
    """
    Converts the given size in bytes to megabytes.

    Parameters:
    size_in_bytes (int): The size to be converted from bytes to megabytes.
    decimal_places (int): The number of decimal places to round the result to.

    Returns:
    float: The size converted to megabytes rounded to 2 decimal places.
    """
    return round(size_in_bytes / 1024 / 1024, decimal_places)
