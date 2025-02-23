import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
import jwt
from datetime import datetime, timedelta, timezone
from starlette.requests import Request

from app.core.config import settings
from app.utils.auth_utils import verify_access_token


# Mock request fixture
@pytest.fixture
def mock_request():
    return MagicMock(spec=Request)

# Mock UserTokenService fixture
@pytest.fixture
def mock_user_token_service():
    return MagicMock()

#Test successful token verification
def test_verify_access_token_valid(mock_request,mock_user_token_service):
    payload = {"sub": "test_user"}
    token = jwt.encode(payload,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    mock_request.headers = {"Authorization": f"Bearer {token}"}

    mock_user_token_service.get_token_active.return_value = MagicMock(
        token=token, expires_at=(datetime.now(timezone.utc) + timedelta(minutes=5)).replace(tzinfo=None)
    )

    decoded_payload=verify_access_token(mock_request,mock_user_token_service)

    assert decoded_payload == payload, "Error: The decoded token payload does not match the expected."

#Test invalid token
def test_verify_access_token_invalid_token(mock_request, mock_user_token_service):
    mock_request.headers = {"Authorization": "Bearer invalid_token"}

    with pytest.raises(HTTPException) as exc_info:
        verify_access_token(mock_request, mock_user_token_service)

    assert exc_info.value.status_code == 401, "Error: Status code should be 401."
    assert exc_info.value.detail == "Token is invalid", "Error: Incorrect error message for invalid token."


#Test expired token
def test_verify_access_token_expired_token(mock_request,mock_user_token_service):
    payload = {"sub": "test_user"}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    mock_request.headers = {"Authorization": f"Bearer {token}"}


    mock_user_token_service.get_token_active.return_value = MagicMock(
        token=token, expires_at=(datetime.now(timezone.utc) - timedelta(minutes=5)).replace(tzinfo=None)
    )

    with pytest.raises(HTTPException) as exc_info:
        verify_access_token(mock_request, mock_user_token_service)

    assert exc_info.value.status_code == 401, "Error: Status code should be 401."
    assert exc_info.value.detail == "Invalid or expired token", "Error: Incorrect error message for expired token."

#Test missing token in Authorization header
def test_verify_access_token_missing_token(mock_request,mock_user_token_service):
    mock_request.headers = {}

    with pytest.raises(HTTPException) as exc_info:
        verify_access_token(mock_request, mock_user_token_service)

    assert exc_info.value.status_code == 401, "Error: Status code should be 401."
    assert exc_info.value.detail == "Missing Authorization header", "Error: Incorrect error message for missing token."

#Test when the Authorization header does not have 'Bearer
def test_verify_access_token_no_bearer(mock_request, mock_user_token_service):
    mock_request.headers = {"Authorization": "SomeOtherToken token_value"}

    with pytest.raises(HTTPException) as exc_info:
        verify_access_token(mock_request, mock_user_token_service)

    assert exc_info.value.status_code == 401, "Error: Status code should be 401."
    assert exc_info.value.detail == "Invalid Authorization header format", "Error: Incorrect error message for missing 'Bearer'."