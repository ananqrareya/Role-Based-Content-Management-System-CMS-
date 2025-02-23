from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.entities.models import Roles
from app.repositories.role_repository import RoleRepository
from app.services.roles_service import RoleService




@pytest.fixture
def role_service(mock_role_repository):
    service = RoleService()
    service.role_repository = mock_role_repository
    return service


def test_create_role_if_not_exist(role_service, mock_role_repository):

    role_name = "Admin"
    mock_role_repository.get_role_by_name.return_value = None

    new_role = Roles(name=role_name, description="Admin Role")
    mock_role_repository.create_role.return_value = new_role

    created_role = role_service.create_role_if_not_exists(role_name)

    assert created_role == new_role
    mock_role_repository.get_role_by_name.assert_called_once_with(role_name)
    mock_role_repository.create_role.assert_called_once()
    assert created_role.name == role_name
    assert created_role.description == "Admin Role"


def test_create_role_if_not_exists_returns_existing_role(role_service, mock_role_repository):

    role_name = "User"
    existing_role = Roles(name=role_name, description="User role")
    mock_role_repository.get_role_by_name.return_value = existing_role

    returned_role = role_service.create_role_if_not_exists(role_name)

    assert returned_role == existing_role
    mock_role_repository.get_role_by_name.assert_called_once_with(role_name)
    mock_role_repository.create_role.assert_not_called()


def test_get_all_role(role_service, mock_role_repository):

    roles = [
        Roles(name="Admin", description="Admin role"),
        Roles(name="User", description="User role"),
    ]

    mock_role_repository.get_all_roles.return_value = roles

    result = role_service.get_all_role()

    assert result == roles
    mock_role_repository.get_all_roles.assert_called_once()


@pytest.mark.parametrize(
    "role_exists, expected_result, raises_exception",
    [
        (True, {"id": uuid4(), "name": "Admin", "users": ["User1", "User2"]}, False),
        (False, None, True),
    ],
)
def test_get_role_with_users(role_service, mock_role_repository, role_exists, expected_result, raises_exception):

    role_id = uuid4()

    if role_exists:
        role = Roles(id=role_id, name="Admin", description="Admin role")
        mock_role_repository.get_role_by_id.return_value = role
        mock_role_repository.get_role_with_users.return_value = expected_result

        result = role_service.get_role_with_users(role_id)

        assert result == expected_result
        mock_role_repository.get_role_by_id.assert_called_once_with(role_id)
        mock_role_repository.get_role_with_users.assert_called_once()

    else:
        mock_role_repository.get_role_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            role_service.get_role_with_users(role_id)

        assert exc_info.value.status_code == 409
        assert exc_info.value.detail == "Role not found"
        mock_role_repository.get_role_by_id.assert_called_once_with(role_id)
        mock_role_repository.get_role_with_users.assert_not_called()
