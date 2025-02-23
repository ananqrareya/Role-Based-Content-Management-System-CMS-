import pytest
from fastapi import HTTPException
from uuid import UUID
from app.entities.models import Categories
from app.entities.schemas.category_schema import CategoryCreate, CategoryUpdate
from app.services.categories_service import CategoriesService


@pytest.fixture
def categories_service(mock_categories_repository, mock_db):
    service = CategoriesService(db=mock_db)
    service.categories_repository = mock_categories_repository
    return service


@pytest.mark.parametrize(
    "category_name, category_description, category_exists, should_raise_exception",
    [
        ("Tech", "Technology articles", False, False),
        ("Tech", "Technology articles", True, True),
    ],
)
def test_create_category(
    categories_service,
    mock_categories_repository,
    category_name,
    category_description,
    category_exists,
    should_raise_exception,
):
    category_data = CategoryCreate(name=category_name, description=category_description)

    mock_categories_repository.check_category_exists.return_value = category_exists

    if should_raise_exception:
        with pytest.raises(ValueError) as exc_info:
            categories_service.create_category(category_data)
        assert (
            str(exc_info.value) == f"Category with name {category_name} already exists"
        )
    else:
        categories_service.create_category(category_data)

        mock_categories_repository.add_category.assert_called_once()

        called_category = mock_categories_repository.add_category.call_args[0][0]
        assert called_category.name == category_name
        assert called_category.description == category_description


@pytest.mark.parametrize(
    "category_id, category_exists, should_raise_exception",
    [
        (UUID("550e8400-e29b-41d4-a716-446655440000"), True, False),
        (UUID("550e8400-e29b-41d4-a716-446655440001"), False, True),
    ],
)
def test_update_category(
    categories_service,
    mock_categories_repository,
    category_id,
    category_exists,
    should_raise_exception,
):
    category_update_data = CategoryUpdate(
        name="Updated Tech", description="Updated description"
    )

    if category_exists:

        mock_category_old = Categories(
            id=category_id, name="Old Tech", description="Old description"
        )
        mock_categories_repository.get_category_by_id.return_value = mock_category_old

        mock_updated_category = Categories(
            id=category_id,
            name=category_update_data.name,
            description=category_update_data.description,
        )
        mock_categories_repository.update_category.return_value = mock_updated_category

        result = categories_service.update_category(category_id, category_update_data)

        assert result == mock_updated_category
        mock_categories_repository.get_category_by_id.assert_called_once_with(
            category_id
        )
        mock_categories_repository.update_category.assert_called_once_with(
            mock_category_old, category_update_data
        )

    else:

        mock_categories_repository.get_category_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            categories_service.update_category(category_id, category_update_data)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Category not found"
        mock_categories_repository.get_category_by_id.assert_called_once_with(
            category_id
        )


@pytest.mark.parametrize(
    "category_id, category_exists, should_raise_exception",
    [
        (UUID("550e8400-e29b-41d4-a716-446655440000"), True, False),
        (UUID("550e8400-e29b-41d4-a716-446655440001"), False, True),
    ],
)
def test_delete_category(
    categories_service,
    mock_categories_repository,
    category_id,
    category_exists,
    should_raise_exception,
):
    if category_exists:

        mock_category = Categories(
            id=category_id, name="Tech", description="Technology articles"
        )
        mock_categories_repository.get_category_by_id.return_value = mock_category

        result = categories_service.delete_category(category_id)

        assert result == mock_category
        mock_categories_repository.get_category_by_id.assert_called_once_with(
            category_id
        )
        mock_categories_repository.delete_category.assert_called_once_with(
            mock_category
        )

    else:

        mock_categories_repository.get_category_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            categories_service.delete_category(category_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Category not found"
        mock_categories_repository.get_category_by_id.assert_called_once_with(
            category_id
        )


@pytest.mark.parametrize(
    "categories_list",
    [
        [
            Categories(
                id=UUID("550e8400-e29b-41d4-a716-446655440000"),
                name="Tech",
                description="Technology articles",
            ),
            Categories(
                id=UUID("550e8400-e29b-41d4-a716-446655440001"),
                name="Health",
                description="Health tips",
            ),
        ],
        [],
    ],
)
def test_get_all_categories(
    categories_service, mock_categories_repository, categories_list
):

    mock_categories_repository.get_all_categories.return_value = categories_list

    result = categories_service.get_all_categories()

    assert result == categories_list
    mock_categories_repository.get_all_categories.assert_called_once()


@pytest.mark.parametrize(
    "category_id, category_exists, should_raise_exception",
    [
        (UUID("550e8400-e29b-41d4-a716-446655440000"), True, False),
        (UUID("550e8400-e29b-41d4-a716-446655440001"), False, True),
    ],
)
def test_get_category_by_id(
    categories_service,
    mock_categories_repository,
    category_id,
    category_exists,
    should_raise_exception,
):
    if category_exists:

        mock_category = Categories(
            id=category_id, name="Tech", description="Technology articles"
        )
        mock_categories_repository.get_category_by_id.return_value = mock_category

        result = categories_service.get_category_by_id(category_id)

        assert result == mock_category
        mock_categories_repository.get_category_by_id.assert_called_once_with(
            category_id
        )

    else:

        mock_categories_repository.get_category_by_id.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            categories_service.get_category_by_id(category_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Category not found"
        mock_categories_repository.get_category_by_id.assert_called_once_with(
            category_id
        )
