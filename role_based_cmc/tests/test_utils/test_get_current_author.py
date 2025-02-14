import pytest
from unittest.mock import MagicMock

from fastapi import HTTPException
from starlette.requests import Request
from uuid import UUID

from app.utils.auth_utils import get_current_author


# Mock Request fixture
@pytest.fixture
def mock_request():
    return MagicMock(spec=Request)


# Mock UserService fixture
@pytest.fixture
def mock_user_service():
    return MagicMock()

#Test getting the current author when user is authenticated
def test_get_current_author_authenticated(mock_request, mock_user_service):
    mock_request.state.user = {"user_id": str(UUID("12345678-1234-1234-1234-1234567890ab"))}

    mock_user_service.get_user_by_id.return_value = {"user_id": "12345678-1234-1234-1234-1234567890ab", "username": "test_user"}

    author = get_current_author(mock_request, mock_user_service)

    assert author["username"] == "test_user", "Error: The returned author does not match the expected user."

#Test when user is not authenticated
def test_get_current_author_not_authenticated(mock_request, mock_user_service):
    mock_request.state.user = None

    with pytest.raises(HTTPException) as exc_info:
        get_current_author(mock_request, mock_user_service)

    assert exc_info.value.status_code == 401, "Error: Status code should be 401."
    assert exc_info.value.detail == "Not authenticated", "Error: Incorrect error message for unauthenticated user."

#Test when user_id is missing in the token
def test_get_current_author_missing_user_id(mock_request, mock_user_service):
    mock_request.state.user = {}

    with pytest.raises(HTTPException) as exc_info:
        get_current_author(mock_request, mock_user_service)

    assert exc_info.value.status_code == 401, "Error: Status code should be 401."
    assert exc_info.value.detail == "Not authenticated", "Error: Incorrect error message for missing user_id."

#Test when user_id format is invalid
def test_get_current_author_invalid_user_id_format(mock_request, mock_user_service):
    mock_request.state.user = {"user_id": "invalid_uuid_format"}

    with pytest.raises(HTTPException) as exc_info:
        get_current_author(mock_request, mock_user_service)

    assert exc_info.value.status_code == 400, "Error: Status code should be 400."
    assert exc_info.value.detail == "Invalid user_id format", "Error: Incorrect error message for invalid user_id format."

#Test when user is not found in the database
def test_get_current_author_user_not_found(mock_request, mock_user_service):
    mock_request.state.user = {"user_id": str(UUID("12345678-1234-1234-1234-1234567890ab"))}

    mock_user_service.get_user_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        get_current_author(mock_request, mock_user_service)

    assert exc_info.value.status_code == 404, "Error: Status code should be 404."
    assert exc_info.value.detail == "Author not found", "Error: Incorrect error message for user not found."