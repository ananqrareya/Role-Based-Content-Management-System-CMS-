from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, ANY


import pytest

from app.entities.models import UserTokens, User
from app.repositories.user_repository import UserRepository
from app.repositories.user_token_repository import UserTokenRepository
from app.services.user_token_service import UserTokenService


@pytest.fixture
def user_token_service(mock_user_repository, mock_token_repository, mock_db):
    service = UserTokenService(db=mock_db)
    service.user_repository = mock_user_repository
    service.token_repository = mock_token_repository
    return service


@pytest.mark.parametrize(
    "user_id, token, expires_at, should_raise_exception",
    [
        (
            "12345",
            "test_token_abc123",
            datetime.now(timezone.utc) + timedelta(days=1),
            False,
        ),
        (
            "12345",
            "test_token_abc123",
            datetime.now(timezone.utc) - timedelta(days=1),
            True,
        ),
        (
            None,
            "test_token_abc123",
            datetime.now(timezone.utc) + timedelta(days=1),
            True,
        ),
        ("12345", None, datetime.now(timezone.utc) + timedelta(days=1), True),
    ],
)
def test_store_user_token(
    user_token_service,
    mock_token_repository,
    user_id,
    token,
    expires_at,
    should_raise_exception,
):
    if should_raise_exception:
        mock_token_repository.save_token.side_effect = Exception("Database error")
        with pytest.raises(Exception):
            user_token_service.store_user_token(user_id, token, expires_at)
    else:
        mock_saved_token = UserTokens(
            user_id=user_id, token=token, expires_at=expires_at, is_active=True
        )
        mock_token_repository.save_token.return_value = mock_saved_token
        result = user_token_service.store_user_token(user_id, token, expires_at)

        assert result == mock_saved_token
        mock_token_repository.save_token.assert_called_once()


@pytest.mark.parametrize(
    "token, token_exists, expected_result",
    [
        (
            "valid_token",
            True,
            UserTokens(
                user_id=1,
                token="valid_token",
                expires_at=datetime.now(timezone.utc),
                is_active=True,
            ),
        ),
        ("invalid_token", False, None),
    ],
)
def test_get_token_active(
    user_token_service, mock_token_repository, token, token_exists, expected_result
):

    mock_token_repository.get_token_is_active.return_value = (
        expected_result if token_exists else None
    )

    result = user_token_service.get_token_active(token)

    assert result == expected_result

    mock_token_repository.get_token_is_active.assert_called_once_with(token)


@pytest.mark.parametrize(
    "username, user_exists, expected_exception",
    [
        ("valid_user", True, None),
        ("invalid_user", False, ValueError),
    ],
)
def test_deactivate_expired_tokens(
    user_token_service,
    mock_user_repository,
    mock_token_repository,
    username,
    user_exists,
    expected_exception,
):
    mock_user_repository.get_user_by_username.return_value = (
        User(username=username) if user_exists else None
    )

    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            user_token_service.deactivate_expired_tokens(username)

        assert str(exc_info.value) == f"User with username '{username}' not found"
    else:
        user_token_service.deactivate_expired_tokens(username)

        mock_token_repository.deactivate_expired_token_of_user.assert_called_once_with(
            mock_user_repository.get_user_by_username.return_value, ANY
        )

    mock_user_repository.get_user_by_username.assert_called_once_with(username)


@pytest.mark.parametrize(
    "token, token_is_active, should_raise_exception",
    [
        ("active_token", True, False),
        ("inactive_token", False, True),
    ],
)
def test_revoke_token(
    user_token_service,
    mock_token_repository,
    token,
    token_is_active,
    should_raise_exception,
):
    token_instance = UserTokens(
        user_id="1",
        token=token,
        expires_at=datetime.now(timezone.utc) + timedelta(days=1),
        is_active=token_is_active,
    )
    mock_token_repository.get_token_is_active.return_value = (
        token_instance if token_is_active else None
    )

    if should_raise_exception:
        with pytest.raises(ValueError) as exc:
            user_token_service.revoke_token(token)
        assert str(exc.value) == f"User with token '{token}' not found"
    else:
        user_token_service.revoke_token(token)
        mock_token_repository.revoke.assert_called_once_with(token_instance)
