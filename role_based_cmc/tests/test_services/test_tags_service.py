import pytest
from app.entities.models import Tags
from app.services.tags_service import TagsService
from uuid import UUID
from app.entities.schemas.tag_schema import TagCreate


@pytest.fixture
def tags_service(mock_tags_repository, mock_db):
    service = TagsService()
    service.tags_repository = mock_tags_repository
    return service


@pytest.mark.parametrize(
    "tag_name, tag_exists, should_raise_exception",
    [
        ("Python", False, False),
        ("Python", True, True),
    ],
)
def test_create_tag(
    tags_service, mock_tags_repository, tag_name, tag_exists, should_raise_exception
):
    tag_data = TagCreate(name=tag_name)

    mock_tags_repository.get_tag_by_name.return_value = tag_exists

    if should_raise_exception:
        with pytest.raises(ValueError) as exc_info:
            tags_service.create_tag(tag_data)
        assert str(exc_info.value) == f"Tag {tag_name} already exists"
    else:
        tags_service.create_tag(tag_data)

        mock_tags_repository.add_tag.assert_called_once()

        called_tag = mock_tags_repository.add_tag.call_args[0][0]
        assert called_tag.name == tag_name


@pytest.mark.parametrize(
    "tag_id, tag_exists, should_raise_exception",
    [
        (UUID("550e8400-e29b-41d4-a716-446655440000"), True, False),
        (UUID("550e8400-e29b-41d4-a716-446655440001"), False, True),
    ],
)
def test_delete_tag(
    tags_service, mock_tags_repository, tag_id, tag_exists, should_raise_exception
):
    if tag_exists:

        mock_tag = Tags(id=tag_id, name="Python")
        mock_tags_repository.get_tag_by_id.return_value = mock_tag

        result = tags_service.delete_tag(tag_id)

        assert result == mock_tag
        mock_tags_repository.get_tag_by_id.assert_called_once_with(tag_id)
        mock_tags_repository.delete_tag.assert_called_once_with(mock_tag)

    else:

        mock_tags_repository.get_tag_by_id.return_value = None

        with pytest.raises(ValueError) as exc_info:
            tags_service.delete_tag(tag_id)

        assert str(exc_info.value) == f"Tag {tag_id} does not exist"
        mock_tags_repository.get_tag_by_id.assert_called_once_with(tag_id)


@pytest.mark.parametrize(
    "tag_id, tag_exists, should_raise_exception",
    [
        (UUID("550e8400-e29b-41d4-a716-446655440000"), True, False),
        (UUID("550e8400-e29b-41d4-a716-446655440001"), False, True),
    ],
)
def test_check_tag(
    tags_service, mock_tags_repository, tag_id, tag_exists, should_raise_exception
):
    if tag_exists:

        mock_tag = Tags(id=tag_id, name="Python")
        mock_tags_repository.get_tag_by_id.return_value = mock_tag

        result = tags_service.check_tag(tag_id)

        assert result is True
        mock_tags_repository.get_tag_by_id.assert_called_once_with(tag_id)

    else:

        mock_tags_repository.get_tag_by_id.return_value = None

        with pytest.raises(ValueError) as exc_info:
            tags_service.check_tag(tag_id)

        assert str(exc_info.value) == f"Tag {tag_id} does not exist"
        mock_tags_repository.get_tag_by_id.assert_called_once_with(tag_id)


@pytest.mark.parametrize(
    "tags_list",
    [
        [
            Tags(id=UUID("550e8400-e29b-41d4-a716-446655440000"), name="Python"),
            Tags(id=UUID("550e8400-e29b-41d4-a716-446655440001"), name="FastAPI"),
        ],
        [],
    ],
)
def test_get_all_tags(tags_service, mock_tags_repository, tags_list):

    mock_tags_repository.get_all_tags.return_value = tags_list

    result = tags_service.get_all_tags()

    assert result == tags_list
    mock_tags_repository.get_all_tags.assert_called_once()
