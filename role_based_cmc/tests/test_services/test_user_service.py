from unittest.mock import MagicMock
import pytest
from fastapi import HTTPException
from uuid import uuid4
from app.entities.models import Roles
from app.entities.schemas.user_schema import RegisterRequest
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.entities.models.User import User
from app.utils.password_utils import hash_password




@pytest.fixture
def user_service(mock_user_repository, mock_role_repository):
    service = UserService()
    service.user_repository = mock_user_repository
    service.role_repository = mock_role_repository
    return service


@pytest.mark.parametrize(
    "email_exists, role_exists, expected_exception",
    [
        (False, True, None),
        (True, True, ValueError),
        (False, False, ValueError),
    ],
)
def test_create_admin_user(user_service, mock_user_repository, mock_role_repository, email_exists, role_exists,
                           expected_exception):
    email = "admin@example.com"
    username = "admin_user"
    password = "securepassword1"
    role_name = "Admin"


    mock_user_repository.get_user_by_email.return_value = User(email=email) if email_exists else None


    role = Roles(name=role_name,description="role admin") if role_exists else None
    mock_role_repository.get_role_by_name.return_value = role

    if expected_exception:
        with pytest.raises(expected_exception):
            user_service.create_admin_user(email, username, password, role_name)
    else:
        mock_user_repository.create_user.return_value = User(email=email, username=username,
                                                             password=hash_password(password), role_id=1)
        created_user = user_service.create_admin_user(email, username, password, role_name)

        assert created_user.email == email
        assert created_user.username == username
        assert mock_user_repository.create_user.called


@pytest.mark.parametrize(
    "email_exists, username_exists, role_exists, role_name, expected_exception, expected_active",
    [
        (False, False, True, "User", None, True),
        (True, False, True, "User", ValueError, None),
        (False, True, True, "User", ValueError, None),
        (False, False, False, "InvalidRole", HTTPException, None),
        (False, False, True, "Author", None, False),
    ],
)
def test_register_user(user_service, mock_user_repository, mock_role_repository, email_exists, username_exists,
                       role_exists, role_name, expected_exception, expected_active):
    user_data = RegisterRequest(
        email="test@example.com",
        username="testuser",
        password="SecurePassword1!",
        role=role_name,
    )

    mock_user_repository.get_user_by_email.return_value = User(email=user_data.email) if email_exists else None
    mock_user_repository.get_user_by_username.return_value = User(
        username=user_data.username) if username_exists else None

    role = Roles(name=role_name, id=1) if role_exists else None
    mock_role_repository.get_role_by_name.return_value = role

    if expected_exception:
        with pytest.raises(expected_exception):
            user_service.register_user(user_data)
    else:
        mock_user_repository.create_user.return_value = User(
            email=user_data.email,
            username=user_data.username,
            password=hash_password(user_data.password),
            role_id=role.id,
            is_active=expected_active,
        )

        created_user = user_service.register_user(user_data)

        assert created_user.email == user_data.email
        assert created_user.username == user_data.username
        assert created_user.is_active == expected_active
        mock_user_repository.create_user.assert_called_once()


@pytest.mark.parametrize(
    "user_exists, password_is_correct, is_active, expected_exception, expected_status_code",
    [
        (True, True, True, None, None),
        (False, None, None, HTTPException, 401),
        (True, False, None, HTTPException, 403),
        (True, True, False, HTTPException, 403),
    ],
)
def test_authenticate_user(
    user_service,
    mock_user_repository,
    user_exists,
    password_is_correct,
    is_active,
    expected_exception,
    expected_status_code
):
    username = "testuser"
    password = "securepassword"


    user_data = User(username=username, email="test@example.com", password=hash_password(password), is_active=is_active)
    mock_user_repository.get_user_by_username.return_value = user_data if user_exists else None

    if password_is_correct:
        mock_user_repository.get_user_by_username.return_value.password = hash_password(password)

    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            user_service.authenticate_user(username, password)

        assert exc_info.value.status_code == expected_status_code
        assert exc_info.value.detail == ("Invalid username or password" if expected_status_code == 401 else "User account is inactive")
    else:
        authenticated_user = user_service.authenticate_user(username, password)
        assert authenticated_user == user_data
        mock_user_repository.get_user_by_username.assert_called_once_with(username)



@pytest.mark.parametrize(
    "username, user_exists, expected_status_code, expected_detail",
    [
        ("testuser", True, None, None),
        ("nonexistentuser", False, 404, "User not found"),
    ]
)
def test_get_user_by_username(user_service, mock_user_repository, username, user_exists, expected_status_code, expected_detail):
    user_data = User(username=username, email="test@example.com", password="hashed_password") if user_exists else None
    mock_user_repository.get_user_by_username.return_value = user_data

    if expected_status_code:
        with pytest.raises(HTTPException) as exc_info:
            user_service.get_user_by_username(username)

        assert exc_info.value.status_code == expected_status_code
        assert exc_info.value.detail == expected_detail
    else:
        user = user_service.get_user_by_username(username)
        assert user == user_data


@pytest.mark.parametrize(
    "users_data, expected_result",
    [
        (
            [
                User(username="testuser1", email="test1@example.com", password="hashed_password"),
                User(username="testuser2", email="test2@example.com", password="hashed_password")
            ],
            2
        ),

        (
            [],
            0
        )
    ]
)
def test_get_all_users(user_service, mock_user_repository, users_data, expected_result):
    mock_user_repository.get_all_user.return_value = users_data

    users = user_service.get_all_users()

    assert len(users) == expected_result
    mock_user_repository.get_all_user.assert_called_once()


@pytest.mark.parametrize(
    "user_data, expected_status_code, expected_detail",
    [
        (User(username="testuser", email="test@example.com", password="hashed_password"), None, None),
        (None, 404, "User not found")
    ]
)
def test_get_user_by_id(user_service, mock_user_repository, user_data, expected_status_code, expected_detail):
    user_id = uuid4()
    mock_user_repository.get_user_by_id.return_value = user_data

    if expected_status_code:
        with pytest.raises(HTTPException) as exc_info:
            user_service.get_user_by_id(user_id)

        assert exc_info.value.status_code == expected_status_code
        assert exc_info.value.detail == expected_detail
    else:
        user = user_service.get_user_by_id(user_id)
        assert user == user_data

@pytest.mark.parametrize(
    "inactive_users_data, expected_result",
    [

        (
            [
                User(username="testuser1", email="test1@example.com", password="hashed_password", is_active=False),
                User(username="testuser2", email="test2@example.com", password="hashed_password", is_active=False)
            ],
            2
        ),

        (
            [],
            0
        )
    ]
)
def test_get_users_inactive(user_service, mock_user_repository, inactive_users_data, expected_result):

    mock_user_repository.get_user_inactive.return_value = inactive_users_data


    inactive_users = user_service.get_users_inactive()


    assert len(inactive_users) == expected_result
    mock_user_repository.get_user_inactive.assert_called_once()


@pytest.mark.parametrize(
    "user_data, role_data, user_exists, role_exists, expected_exception, expected_status_code, expected_detail",
    [
        (User(username="testuser", email="test@example.com", password="hashed_password", is_active=True),
         Roles(name="Admin", description="Administrator role"), True, True, None, None, None),

        (None, None, False, True, HTTPException, 404, "User not found"),

        (User(username="testuser", email="test@example.com", password="hashed_password", is_active=True),
         None, True, False, HTTPException, 404, "Role 'Admin' does not exist"),
    ]
)
def test_update_role(user_service, mock_user_repository, mock_role_repository, user_data, role_data,
                     user_exists, role_exists, expected_exception, expected_status_code, expected_detail):
    user_id = uuid4()
    mock_user_repository.get_user_by_id.return_value = user_data if user_exists else None
    mock_role_repository.get_role_by_name.return_value = role_data if role_exists else None

    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            user_service.update_role(user_id, "Admin")

        assert exc_info.value.status_code == expected_status_code
        assert exc_info.value.detail == expected_detail
    else:
        user_service.update_role(user_id, "Admin")
        mock_user_repository.update_role_user.assert_called_once_with(user_data, role_data)


@pytest.mark.parametrize(
    "user_data, user_exists, is_active, expected_exception, expected_status_code, expected_detail",
    [

        (User(username="testuser", email="test@example.com", password="hashed_password", is_active=False), True, False,
         None, None, None),


        (User(username="testuser", email="test@example.com", password="hashed_password", is_active=True), True, True,
         HTTPException, 403, "User account already is active"),


        (None, False, False, HTTPException, 404, "User not found"),
    ]
)
def test_activate_user(user_service, mock_user_repository, user_data, user_exists, is_active, expected_exception,
                       expected_status_code, expected_detail):
    user_id = uuid4()

    mock_user_repository.get_user_by_id.return_value = user_data if user_exists else None

    if expected_exception:

        with pytest.raises(expected_exception) as exc_info:
            user_service.activate_user(user_id)

        assert exc_info.value.status_code == expected_status_code
        assert exc_info.value.detail == expected_detail
    else:
        user_service.activate_user(user_id)
        mock_user_repository.active_user.assert_called_once_with(user_data)


@pytest.mark.parametrize(
    "user_data, user_exists, expected_exception, expected_status_code, expected_detail",
    [

        (User(username="testuser", email="test@example.com", password="hashed_password", is_active=True), True, None,
         None, None),


        (None, False, HTTPException, 404, "User not found"),
    ]
)
def test_delete_user(user_service, mock_user_repository, user_data, user_exists, expected_exception,
                     expected_status_code, expected_detail):
    user_id = uuid4()

    mock_user_repository.get_user_by_id.return_value = user_data if user_exists else None

    if expected_exception:

        with pytest.raises(expected_exception) as exc_info:
            user_service.delete_user(user_id)

        assert exc_info.value.status_code == expected_status_code
        assert exc_info.value.detail == expected_detail
    else:
        user_service.delete_user(user_id)
        mock_user_repository.delete_user.assert_called_once()
