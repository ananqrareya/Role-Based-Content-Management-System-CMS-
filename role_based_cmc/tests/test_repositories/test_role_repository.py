import pytest
from sqlalchemy.exc import IntegrityError
from app.entities.enums.RoleEnum import RoleEnum
from app.entities.models import Roles, User
from app.repositories.role_repository import RoleRepository


def create_role(db_session, name, description="Default role description"):
    role = Roles(name=name, description=description)
    db_session.add(role)
    db_session.commit()
    return role


@pytest.fixture
def repository(db_session):
    return RoleRepository(db_session)


def test_create_role_success(db_session, repository):

    new_role = create_role(db_session, RoleEnum.ADMIN, "Administrator role")

    fetched_role = repository.get_role_by_name(new_role.name)

    assert fetched_role is not None
    assert fetched_role.id is not None
    assert fetched_role.name == RoleEnum.ADMIN
    assert fetched_role.description == "Administrator role"


def test_create_role_duplicate(db_session, repository):

    create_role(db_session, RoleEnum.AUTHOR, "Test Description")

    duplicate_role = Roles(name=RoleEnum.AUTHOR, description="Another description")

    with pytest.raises(IntegrityError):
        repository.create_role(duplicate_role)


def test_get_all_roles(db_session, repository):

    assert repository.get_all_roles() == []

    create_role(db_session, RoleEnum.ADMIN, "Administrator role")
    create_role(db_session, RoleEnum.READER, "Regular user role")

    roles = repository.get_all_roles()

    assert len(roles) == 2

    role_names = {role.name for role in roles}
    assert RoleEnum.ADMIN.value in role_names
    assert RoleEnum.READER.value in role_names


def test_get_role_with_users(db_session, repository):

    role = create_role(db_session, RoleEnum.EDITOR, "Editor Role")

    user1 = User(
        username="john_doe",
        email="john.doe@example.com",
        password="hashed_password",
        role_id=role.id,
        is_active=True,
    )

    user2 = User(
        username="jane_smith",
        email="jane.smith@example.com",
        password="hashed_password",
        role_id=role.id,
        is_active=True,
    )

    db_session.add_all([user1, user2])
    db_session.commit()

    fetched_role = repository.get_role_with_users(role)

    assert fetched_role is not None
    assert fetched_role.name == RoleEnum.EDITOR

    user_names = {user.username for user in fetched_role.users}
    assert "john_doe" in user_names
    assert "jane_smith" in user_names


@pytest.mark.parametrize(
    "role_name, expected",
    [
        (RoleEnum.EDITOR, True),
        (RoleEnum.READER, False),
    ],
)
def test_get_role_by_name(db_session, repository, role_name, expected):

    if expected:
        role = create_role(db_session, role_name)
        fetched_role = repository.get_role_by_name(role.name)
        assert fetched_role is not None, f"Role {role_name} should exist"
        assert fetched_role.name == role.name
    else:
        fetched_role = repository.get_role_by_name(role_name)
        assert fetched_role is None, f"Role {role_name} should not exist"
