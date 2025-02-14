from unittest.mock import MagicMock
import jwt
import pytest
from datetime import datetime, timedelta, timezone
from jwt import decode
from app.core.config import settings
from app.utils.auth_utils import create_access_token

@pytest.fixture
def mock_user_service():
    """Mock UserService"""
    mock=MagicMock()
    mock.get_user_by_username.return_value=MagicMock(id=1, username="test_user")
    return mock

@pytest.fixture
def mock_user_token_service():
    """Mock UserTokenService"""
    return MagicMock()


    #Test successful token creation
def test_create_access_token_success(mock_user_service, mock_user_token_service):
    data={"sub":"test_user"}
    token=create_access_token(data,mock_user_service,mock_user_token_service)

    decoded_token=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])

    assert isinstance(token,str), "Error: Token must be a string."
    assert "exp" in decoded_token, "Error: Token must have an expiration time."
    assert decoded_token["sub"]==data["sub"], "Error: Token must have sub string."

    mock_user_service.get_user_by_username.assert_called_with(data["sub"])
    mock_user_token_service.store_user_token.assert_called_once()


    #Test when user is not found in the system
def test_create_access_token_missing_user(mock_user_service, mock_user_token_service):
    mock_user_service.get_user_by_username.return_value=None
    data={"sub":"unknown_user"}
    with pytest.raises(ValueError, match="User not found"):
        create_access_token(data,mock_user_service,mock_user_token_service)

    mock_user_token_service.store_user_token.assert_not_called()


    #Test if the token expiry is set correctly
def test_create_access_token_expiry(mock_user_service, mock_user_token_service):
    data={"sub":"test_user"}
    token=create_access_token(data,mock_user_service,mock_user_token_service)

    decoded_token=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])

    expiration_time = datetime.fromtimestamp(decoded_token["exp"], tz=timezone.utc)

    expected_expiry = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    assert abs((expected_expiry - expiration_time).total_seconds()) < 10, "Error: Token expiration time mismatch."



    #Test when invalid data (no 'sub') is provided
def test_create_access_token_invalid_data(mock_user_service, mock_user_token_service):
    data={}

    with pytest.raises(KeyError, match="'sub'"):
        create_access_token(data,mock_user_service,mock_user_token_service)


    #Ensure service calls happen correctly
def test_create_access_token_mock_calls(mock_user_service, mock_user_token_service):
    data={"sub":"test_user"}

    create_access_token(data,mock_user_service,mock_user_token_service)
    mock_user_service.get_user_by_username.assert_called_once_with("test_user")
    mock_user_token_service.store_user_token.assert_called_once()
