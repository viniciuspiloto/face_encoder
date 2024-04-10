import hashlib
from unittest.mock import patch

from utils.helpers.session_utils import convert_bytes_to_megabytes, generate_unique_id


def test_generate_unique_id():
    """Test case for the generate_unique_id function"""
    with patch("utils.helpers.session_utils.time") as mock_time, patch(
        "utils.helpers.session_utils.uuid"
    ) as mock_uuid:
        mock_time.time.return_value = 1234567890.123456
        mock_uuid.uuid4.return_value = "random_string"
        expected_id = hashlib.md5("1234567890.123456random_string".encode()).hexdigest()
        assert generate_unique_id() == expected_id


def test_convert_bytes_to_megabytes():
    """Test case for the convert_bytes_to_megabytes function"""
    assert convert_bytes_to_megabytes(1048576) == 1.0
    assert convert_bytes_to_megabytes(5242880) == 5.0
