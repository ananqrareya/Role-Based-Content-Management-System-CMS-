import pytest
from uuid import uuid4
from app.entities.models import Categories
from app.entities.schemas.category_schema import CategoryUpdate
from app.repositories.categories_repository import CategoriesRepository


def create_category(db_session, name="Test Category", description="Test Description"):

    new_category = Categories(name=name, description=description)
    db_session.add(new_category)
    db_session.commit()
    db_session.refresh(new_category)
    return new_category


@pytest.fixture
def repository(db_session):
    return CategoriesRepository(db_session)


@pytest.mark.parametrize(
    "create_category_func, should_exist", [(True, True), (False, False)]
)
def test_get_category_by_id(db_session, repository, create_category_func, should_exist):

    category_id = None

    if create_category_func:
        new_category = create_category(db_session)
        category_id = new_category.id
    else:
        category_id = uuid4()

    fetched_category = repository.get_category_by_id(category_id)

    if should_exist:
        assert fetched_category is not None
        assert fetched_category.id == category_id
        assert fetched_category.name == "Test Category"
        assert fetched_category.description == "Test Description"
    else:
        assert fetched_category is None


@pytest.mark.parametrize(
    "name, description, should_raise_exception",
    [
        ("Test Category", "Test Description", False),
        (None, "Invalid Category", True),
    ],
)
def test_add_category(
    repository, db_session, name, description, should_raise_exception
):

    category = Categories(id=uuid4(), name=name, description=description)

    if should_raise_exception:
        with pytest.raises(Exception):
            repository.add_category(category)
        db_session.rollback()

        fetched_category = (
            db_session.query(Categories).filter_by(description=description).first()
        )
        assert fetched_category is None
    else:
        result = repository.add_category(category)
        assert result is not None
        assert isinstance(result, Categories)

        fetched_category = repository.get_category_by_id(result.id)
        assert fetched_category is not None
        assert fetched_category.name == name
        assert fetched_category.description == description
        assert result == fetched_category


@pytest.mark.parametrize(
    "name, description, should_exist",
    [
        ("Test Category", "A valid category", True),
        ("Nonexistent Category", None, False),
    ],
)
def test_get_category_by_name(db_session, repository, name, description, should_exist):

    if should_exist:
        new_category = create_category(db_session, name=name, description=description)
    else:
        new_category = None

    fetched_category = repository.get_category_by_name(name)

    if should_exist:
        assert fetched_category is not None
        assert fetched_category.name == name
        assert fetched_category.description == description
    else:
        assert fetched_category is None


@pytest.mark.parametrize(
    "category_data, expected_count",
    [
        ([("Category 1", "Description 1"), ("Category 2", "Description 2")], 2),
        ([], 0),
    ],
)
def test_get_all_categories(db_session, repository, category_data, expected_count):

    for name, description in category_data:
        category = create_category(db_session, name=name, description=description)

    fetched_categories = repository.get_all_categories()

    assert fetched_categories is not None
    assert isinstance(fetched_categories, list)
    assert len(fetched_categories) == expected_count

    if expected_count > 0:
        for i, category in enumerate(fetched_categories):
            assert category.name == category_data[i][0]
            assert category.description == category_data[i][1]


@pytest.mark.parametrize(
    "category_name, should_exist",
    [("Existing Category", True), ("Nonexistent Category", False)],
)
def test_check_category_exists(db_session, repository, category_name, should_exist):

    if should_exist:

        new_category = create_category(
            db_session, name=category_name, description="A sample category"
        )

    result = repository.check_category_exists(category_name)

    if should_exist:
        assert result is not None
    else:
        assert result is None


@pytest.mark.parametrize(
    "update_data, expected_name, expected_description",
    [
        ({"name": "Updated Name"}, "Updated Name", "Test Description"),
        (
            {"description": "Updated Description"},
            "Test Category",
            "Updated Description",
        ),
        (
            {"name": "New Name", "description": "New Description"},
            "New Name",
            "New Description",
        ),
        ({}, "Test Category", "Test Description"),
    ],
)
def test_update_category(
    db_session, repository, update_data, expected_name, expected_description
):

    category = create_category(db_session)

    category_update = CategoryUpdate(**update_data)

    updated_category = repository.update_category(category, category_update)

    assert updated_category is not None
    assert updated_category.id == category.id
    assert updated_category.name == expected_name
    assert updated_category.description == expected_description


def test_update_nonexistent_category(db_session, repository):

    non_existent_category = Categories(
        name="Does Not Exist", description="No Description"
    )

    category_update = CategoryUpdate(name="New Name")

    with pytest.raises(Exception):
        repository.update_category(non_existent_category, category_update)


def test_delete_category_success(db_session, repository):
    category = create_category(db_session)

    deleted_category = repository.delete_category(category)

    assert deleted_category is not None
    assert deleted_category.id == category.id

    fetched_category = db_session.query(Categories).filter_by(id=category.id).first()
    assert fetched_category is None


def test_delete_category_not_found(db_session, repository):

    non_existent_category = Categories(name="Nonexistent", description="Does not exist")

    with pytest.raises(Exception):
        repository.delete_category(non_existent_category)
