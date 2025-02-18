import pytest
from uuid import uuid4
from app.repositories.article_comment_repository import ArticleCommentRepository
from app.entities.models import Comments, Articles, User
from app.entities.enums import ArticleStatus


@pytest.fixture
def repository(db_session):
    return ArticleCommentRepository(db_session)


def create_user(db_session):

    user = User(
        username=f"user_{uuid4()}",
        email=f"{uuid4()}@example.com",
        password="test_password",
    )
    db_session.add(user)
    db_session.commit()
    return user


def create_article(
    db_session,
    title="Test Article",
    content="Test Content",
    status=ArticleStatus.DRAFT,
    author=None,
):

    if not author:
        author = create_user(db_session)

    article = Articles(title=title, content=content, status=status, author_id=author.id)
    db_session.add(article)
    db_session.commit()
    db_session.refresh(article)
    return article


def create_comment(
    db_session, content="This is a test comment", article=None, user=None
):

    if not article:
        article = create_article(db_session)
    if not user:
        user = create_user(db_session)

    comment = Comments(content=content, article_id=article.id, user_id=user.id)
    db_session.add(comment)
    db_session.commit()
    db_session.refresh(comment)
    return comment


@pytest.mark.parametrize(
    "content, should_raise_exception",
    [
        ("This is a valid comment.", False),
        (None, True),
    ],
)
def test_save_comment(db_session, repository, content, should_raise_exception):

    article = create_article(db_session)
    user = create_user(db_session)

    comment = Comments(content=content, article_id=article.id, user_id=user.id)

    if should_raise_exception:
        with pytest.raises(Exception):
            repository.save_comment(comment)
        db_session.rollback()

        fetched_comment = db_session.query(Comments).filter_by(content=content).first()
        assert fetched_comment is None
    else:
        result = repository.save_comment(comment)

        assert result is not None
        assert isinstance(result, Comments)

        fetched_comment = db_session.query(Comments).filter_by(id=result.id).first()
        assert fetched_comment is not None
        assert fetched_comment.content == content
        assert fetched_comment.article_id == article.id
        assert fetched_comment.user_id == user.id
        assert result == fetched_comment


@pytest.mark.parametrize(
    "should_create, should_exist",
    [
        (True, True),
        (False, False),
    ],
)
def test_get_comment_by_id(db_session, repository, should_create, should_exist):

    comment_id = None
    if should_create:
        comment = create_comment(db_session)
        comment_id = comment.id
    else:
        comment_id = uuid4()
    fetched_comment = repository.get_comment_by_id(comment_id)

    if should_exist:
        assert fetched_comment is not None
        assert fetched_comment.id == comment_id
    else:
        assert fetched_comment is None


@pytest.mark.parametrize(
    "initial_content, new_content, should_change",
    [
        ("This is the original comment.", "This is the updated comment.", True),
        ("Another comment", "Another comment", False),
    ],
)
def test_update_comment(
    db_session, repository, initial_content, new_content, should_change
):

    comment = create_comment(db_session, content=initial_content)

    updated_comment = repository.update_comment(comment, new_content)

    assert updated_comment is not None
    assert updated_comment.id == comment.id
    assert updated_comment.content == new_content

    if should_change:
        assert updated_comment.content != initial_content
    else:
        assert updated_comment.content == initial_content


def test_update_nonexistent_comment(db_session, repository):

    non_existent_comment = Comments(id=uuid4(), content="Nonexistent comment")

    with pytest.raises(Exception):
        repository.update_comment(non_existent_comment, "Trying to update")


def test_delete_comment_success(db_session, repository):

    comment = create_comment(db_session)

    deleted_comment = repository.delete_comment(comment)

    assert deleted_comment is not None
    assert deleted_comment.id == comment.id

    fetched_comment = db_session.query(Comments).filter_by(id=comment.id).first()
    assert fetched_comment is None


def test_delete_comment_not_found(db_session, repository):

    non_existent_comment = Comments(id=uuid4(), content="Nonexistent comment")

    with pytest.raises(ValueError, match="Comment does not exist."):
        repository.delete_comment(non_existent_comment)
