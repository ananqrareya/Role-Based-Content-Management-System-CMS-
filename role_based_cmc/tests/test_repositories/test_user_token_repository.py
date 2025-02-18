import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy.exc import IntegrityError
from app.entities.enums.RoleEnum import RoleEnum
from app.entities.models import Roles, User, UserTokens
from app.repositories.user_token_repository import UserTokenRepository


def create_user(
    db_session,
    username="anan_test",
    email="anan.test@example.com",
    is_active=True,
):
    role = db_session.query(Roles).filter_by(name=RoleEnum.AUTHOR).first()
    if not role:
        role = Roles(name=RoleEnum.AUTHOR)
        db_session.add(role)
        db_session.commit()

    user = User(
        username=username,
        email=email,
        password="test_password",
        role_id=role.id,
        is_active=is_active,
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def repository(db_session):
    return UserTokenRepository(db_session)


def test_save_token(db_session, repository):
    user = create_user(db_session)

    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

    token = UserTokens(
        user_id=user.id, token="sample_token_12345", expires_at=expires_at
    )
    saved_token = repository.save_token(token)

    assert saved_token is not None, "Token was not saved successfully"
    assert saved_token.token == "sample_token_12345", "Token mismatch"

    fetched_token = (
        db_session.query(UserTokens).filter_by(token="sample_token_12345").first()
    )

    assert fetched_token is not None, "Token not found in database"
    assert fetched_token.token == "sample_token_12345", "Fetched token mismatch"


def test_save_token_error(db_session, repository):
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

    invalid_token = UserTokens(
        user_id=None, token="invalid_token_12345", expires_at=expires_at
    )
    with pytest.raises(IntegrityError):
        repository.save_token(invalid_token)


@pytest.mark.parametrize(
    "token_value, expected_active",
    [
        ("sample_token_12345", True),
        ("invalid_token_67890", False),
    ],
)
def test_get_token_is_active(db_session, repository, token_value, expected_active):
    user = create_user(db_session)

    if expected_active:
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        active_token = UserTokens(
            user_id=user.id, token=token_value, expires_at=expires_at
        )
        repository.save_token(active_token)

    token = repository.get_token_is_active(token_value)

    if expected_active:
        assert token is not None, f"Token {token_value} should be active"
        assert token.token == token_value, "Token mismatch"
        assert token.is_active is True, "Token should be active"
    else:
        assert token is None, f"Token {token_value} should not exist"


def test_deactivate_expired_token_of_user(db_session, repository):
    user = create_user(db_session)

    expired_token = UserTokens(
        user_id=user.id,
        token="sample_token_12345",
        expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
        is_active=True,
    )
    valid_token = UserTokens(
        user_id=user.id,
        token="valid_token_456",
        expires_at=datetime.now(timezone.utc) + timedelta(days=1),
        is_active=True,
    )

    db_session.add_all([expired_token, valid_token])
    db_session.commit()

    repository.deactivate_expired_token_of_user(user, datetime.now(timezone.utc))

    active_tokens = (
        db_session.query(UserTokens).filter_by(user_id=user.id, is_active=True).all()
    )

    assert len(active_tokens) == 1, "Only one active token should remain"
    assert active_tokens[0].token == "valid_token_456", "Wrong token was deactivated"


def test_revoke_token(db_session, repository):

    user = create_user(db_session)

    token = UserTokens(
        user_id=user.id,
        token="test_token_789",
        expires_at=datetime.now(timezone.utc) + timedelta(days=1),
        is_active=True,
    )

    db_session.add(token)
    db_session.commit()

    token_in_db = db_session.query(UserTokens).filter_by(token="test_token_789").first()
    assert token_in_db is not None, "Token should exist before revocation"
    assert token_in_db.is_active is True, "Token should be active before revocation"

    repository.revoke(token_in_db)

    updated_token = (
        db_session.query(UserTokens).filter_by(token="test_token_789").first()
    )

    assert updated_token is not None, "Token should still exist after revocation"
    assert updated_token.is_active is False, "Token should be inactive after revocation"
