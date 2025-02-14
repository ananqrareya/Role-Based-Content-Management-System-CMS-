from unittest.mock import MagicMock
import pytest
from fastapi import HTTPException
from starlette.requests import Request

from app.utils.auth_utils import get_token_from_request


# Mock request fixture
@pytest.fixture
def mock_request():
    return MagicMock(spec=Request)

#Test that the function returns the token when the header is valid
def test_get_token_from_request_valid(mock_request):
    mock_request.headers = {"Authorization": "Bearer valid_token_123"}

    token=get_token_from_request(mock_request)

    assert token == "valid_token_123", "Error: The returned token should match the expected token."

#Test when the Authorization header is missing
def test_get_token_from_request_missing_header(mock_request):
    mock_request.headers = {}

    with pytest.raises(HTTPException) as exc_info:
        get_token_from_request(mock_request)

    assert exc_info.value.status_code == 401, "Error: Status code should be 401."
    assert exc_info.value.detail == "Missing Authorization header", "Error: Incorrect error message for missing header."

#Test when the Authorization header has an invalid format
def test_get_token_from_request_invalid_format(mock_request):
    mock_request.headers = {"Authorization": "InvalidHeader invalid_token"}

    with pytest.raises(HTTPException) as exc_info:
        get_token_from_request(mock_request)

    assert exc_info.value.status_code == 401, "Error: Status code should be 401."
    assert exc_info.value.detail == "Invalid Authorization header format", "Error: Incorrect error message for invalid format."

#Test when the Authorization header is missing the 'Bearer' part
def test_get_token_from_request_no_bearer(mock_request):
    mock_request.headers = {"Authorization": "SomeOtherToken token_value"}

    with pytest.raises(HTTPException) as exc_info:
        get_token_from_request(mock_request)

    assert exc_info.value.status_code == 401, "Error: Status code should be 401."
    assert exc_info.value.detail == "Invalid Authorization header format", "Error: Incorrect error message for missing 'Bearer'."