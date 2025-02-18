import pytest
from uuid import uuid4
from app.entities.models import Tags
from app.repositories.tags_repository import TagsRepository


@pytest.fixture
def repository(db_session):
    return TagsRepository(db_session)


def create_tag(db_session, name="Test Tag"):

    new_tag = Tags(name=name)
    db_session.add(new_tag)
    db_session.commit()
    db_session.refresh(new_tag)
    return new_tag


@pytest.mark.parametrize(
    "tag_name, should_exist",
    [
        ("Existing Tag", True),
        ("Nonexistent Tag", False),
    ],
)
def test_get_tag_by_name(db_session, repository, tag_name, should_exist):


    if should_exist:
        create_tag(db_session, name=tag_name)

    fetched_tag = repository.get_tag_by_name(tag_name)

    if should_exist:
        assert fetched_tag is not None
        assert fetched_tag.name == tag_name
    else:
        assert fetched_tag is None



@pytest.mark.parametrize(
    "should_create, should_exist",
    [
        (True, True),
        (False, False),
    ],
)
def test_get_tag_by_id(db_session, repository, should_create, should_exist):

    tag_id = None
    if should_create:
        tag = create_tag(db_session)
        tag_id = tag.id
    else:
        tag_id = uuid4()
    fetched_tag = repository.get_tag_by_id(tag_id)

    if should_exist:
        assert fetched_tag is not None
        assert fetched_tag.id == tag_id
    else:
        assert fetched_tag is None


@pytest.mark.parametrize(
    "tag_data, expected_count",
    [
        ([("Tag 1"), ("Tag 2")], 2),
        ([], 0),
    ],
)
def test_get_all_tags(db_session, repository, tag_data, expected_count):



    for name in tag_data:
        create_tag(db_session, name=name)

    fetched_tags = repository.get_all_tags()

    assert fetched_tags is not None
    assert isinstance(fetched_tags, list)
    assert len(fetched_tags) == expected_count


    if expected_count > 0:
        for i, tag in enumerate(fetched_tags):
            assert tag.name == tag_data[i]


@pytest.mark.parametrize(
    "tag_name, should_raise_exception",
    [
        ("Valid Tag", False),
        (None, True),
    ],
)
def test_add_tag(db_session, repository, tag_name, should_raise_exception):


    tag = Tags(name=tag_name)

    if should_raise_exception:
        with pytest.raises(Exception):
            repository.add_tag(tag)
        db_session.rollback()


        fetched_tag = db_session.query(Tags).filter_by(name=tag_name).first()
        assert fetched_tag is None
    else:
        result = repository.add_tag(tag)

        assert result is not None
        assert isinstance(result, Tags)

        fetched_tag = repository.get_tag_by_name(tag_name)
        assert fetched_tag is not None
        assert fetched_tag.name == tag_name
        assert result == fetched_tag


@pytest.mark.parametrize(
    "should_create, should_exist",
    [
        (True, True),
        (False, False),
    ],
)
def test_delete_tag(db_session, repository, should_create, should_exist):
    tag = None
    if should_create:
        tag = create_tag(db_session)
    else:
        tag = Tags( name="Nonexistent Tag")

    if should_exist:
        deleted_tag = repository.delete_tag(tag)

        assert deleted_tag is not None
        assert deleted_tag.id == tag.id


        fetched_tag = db_session.query(Tags).filter_by(id=tag.id).first()
        assert fetched_tag is None
    else:
        with pytest.raises(Exception):
            repository.delete_tag(tag)