import pytest
from sqlalchemy.testing.suite.test_reflection import users

from app.entities.enums.RoleEnum import RoleEnum
from app.repositories.user_repository import UserRepository
from app.entities.models import User, Roles


def create_user(
    db_session,
    repository,
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
    return UserRepository(db_session)


def test_create_user(db_session, repository):
    user = create_user(db_session, repository)

    assert user is not None, "User creation failed"
    assert user.id is not None, "User ID should be generated"
    assert user.username == "anan_test", "Username mismatch"
    assert user.email == "anan.test@example.com", "Email mismatch"
    assert user.password == "test_password", "Password mismatch"
    assert user.is_active is True, "User should be active"

    fetched_user = db_session.query(User).filter_by(username="anan_test").first()
    assert fetched_user is not None, "User not found in database"
    assert fetched_user.username == "anan_test", "Fetched user mismatch"


@pytest.mark.parametrize(
    "email, expected",
    [
        ("anan.test@example.com", True),
        ("nonexistent@example.com", False),
    ],
)
def test_get_user_by_email(db_session, repository, email, expected):
    create_user(db_session, repository)

    fetched_user = repository.get_user_by_email(email)

    if expected:
        assert fetched_user is not None, f"User " f"with email {email} should exist"
        assert fetched_user.email == email, "Email mismatch"
    else:
        assert fetched_user is None, f"User with " f"email {email} should not exist"


@pytest.mark.parametrize(
    "username, expected",
    [
        ("anan_test", True),
        ("enad_test", False),
    ],
)
def test_get_user_by_username(db_session, repository, username, expected):
    create_user(db_session, repository)

    fetched_user = repository.get_user_by_username(username)

    if expected:
        assert fetched_user is not None, (
            f"User with " f"username {username} should exist"
        )
        assert fetched_user.username == username, "Username mismatch"
    else:
        assert fetched_user is None, (
            f"User with" f" username {username} should not exist"
        )


@pytest.mark.parametrize(
    "username, should_exist",
    [
        ("anan_test", True),
        ("unknown_user", False),
    ],
)
def test_get_user_by_id(db_session, repository, username, should_exist):
    user = create_user(db_session, repository) if should_exist else None

    user_id = user.id if user else "00000000-0000-0000-0000-000000000000"
    fetched_user = repository.get_user_by_id(user_id)

    if should_exist:
        assert fetched_user is not None, "User not found in database"
        assert fetched_user.id == user.id, "User ID mismatch"
        assert fetched_user.username == user.username, "Username mismatch"
    else:
        assert fetched_user is None, "User should not exist but was found"


@pytest.fixture
def inactive_users(db_session, repository):
    users = [
        create_user(
            db_session,
            repository,
            username="active_user",
            email="active@example.com",
            is_active=True,
        ),
        create_user(
            db_session,
            repository,
            username="inactive_user1",
            email="inactive1@example.com",
            is_active=False,
        ),
        create_user(
            db_session,
            repository,
            username="inactive_user2",
            email="inactive2@example.com",
            is_active=False,
        ),
    ]
    return users


def test_get_user_inactive(db_session, repository, inactive_users):
    inactive_users_list = repository.get_user_inactive()

    assert len(inactive_users_list) == 2, "Expected 2 inactive users"
    assert all(
        user.is_active is False for user in inactive_users_list
    ), "Returned users should be inactive"

    inactive_usernames = {user.username for user in inactive_users_list}
    assert "inactive_user1" in inactive_usernames
    assert "inactive_user2" in inactive_usernames
    assert (
        "active_user" not in inactive_usernames
    ), "Active user should not be in the result"


def test_update_role_user(db_session, repository):
    user = create_user(db_session, repository)

    new_role = Roles(name=RoleEnum.EDITOR)
    db_session.add(new_role)
    db_session.commit()

    update_user = repository.update_role_user(user, new_role)
    assert update_user is not None, "User update failed"
    assert update_user.role_id == new_role.id, "User role was not updated"

    fetched_user = repository.get_user_by_id(user.id)
    assert fetched_user is not None, "User not found in database"
    assert fetched_user.role_id == new_role.id, "Database role update mismatch"


def test_activate_user(db_session, repository):
    user = create_user(db_session, repository, is_active=False)

    activate_user = repository.active_user(user)

    assert activate_user is not None, "User activation failed"
    assert activate_user.is_active is True, "User should be active after update"

    fetched_user = repository.get_user_by_id(user.id)
    assert fetched_user is not None, "User not found in database"
    assert fetched_user.is_active is True, "User should be active in database"


def test_delete_user(db_session, repository):
    user = create_user(db_session, repository)

    repository.delete_user(user)

    fetched_user = repository.get_user_by_id(user.id)
    assert fetched_user is None, "User was not deleted from the database"


def test_delete_nonexistent_user(db_session, repository):
    non_existent_user = User(
        id="00000000-0000-0000-0000-000000000000",
        username="ghost_user",
        email="ghost@example.com",
        password="test_password",
        is_active=True,
    )
    with pytest.raises(ValueError, match="Error deleting user role"):
        repository.delete_user(non_existent_user)
