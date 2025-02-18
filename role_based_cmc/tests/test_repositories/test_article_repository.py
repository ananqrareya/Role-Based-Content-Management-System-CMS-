import pytest
from typing import List
from uuid import uuid4

from docutils.nodes import title, author
from unicodedata import category

from app.entities.enums import ArticleStatus
from app.entities.enums.RoleEnum import RoleEnum
from app.entities.schemas.article_schema import ArticleUpdate
from app.repositories.article_repository import ArticleRepository
from app.entities.models import User, Categories, Articles, Roles
from tests.conftest import db_session


@pytest.fixture
def repository(db_session):
    return ArticleRepository(db_session)


def create_user(db_session):
    role = db_session.query(Roles).filter_by(name=RoleEnum.AUTHOR).first()
    if not role:
        role = Roles(name=RoleEnum.AUTHOR)
        db_session.add(role)
        db_session.commit()

    user = User(
        username=f"test_user_{uuid4().hex[:8]}",
        email=f"{uuid4()}@example.com",
        password="test_password",
        role_id=role.id,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def create_category(db_session, name="Test Category"):
    category = Categories(name=name, description="Test Category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


def create_article(db_session, title, content, status, author, category):

    article = Articles(
        title=title,
        content=content,
        status=status,
        author_id=author.id,
        category_id=category.id if category else None,
    )
    db_session.add(article)
    db_session.commit()
    db_session.refresh(article)
    return article


@pytest.mark.parametrize(
    "title, content, status, include_category, should_raise_exception",
    [
        ("Valid Article", "This is a valid article.", ArticleStatus.DRAFT, True, False),
        (
            "Valid Article No Category",
            "Valid content.",
            ArticleStatus.DRAFT,
            False,
            False,
        ),
        (None, "Missing title", ArticleStatus.DRAFT, True, True),
        ("Missing content", None, ArticleStatus.DRAFT, True, True),
        ("Valid Article", "Valid Content", None, True, True),
    ],
)
def test_add_article(
    db_session,
    repository,
    title,
    content,
    status,
    include_category,
    should_raise_exception,
):
    author = create_user(db_session)
    category = create_category(db_session) if include_category else None

    if should_raise_exception:

        article_invalid = Articles(
            title=None,
            content=content,
            status=status,
            author_id=author.id,
            category_id=category.id if category else None,
        )
        with pytest.raises(Exception):
            repository.add_article(article_invalid)

        db_session.rollback()

        fetched_article = db_session.query(Articles).filter_by(title=title).first()
        assert fetched_article is None
    else:
        article = Articles(
            title=title,
            content=content,
            status=status,
            author_id=author.id,
            category_id=category.id if category else None,
        )
        result = repository.add_article(article)

        assert result is not None
        assert isinstance(result, Articles)

        fetched_article = db_session.query(Articles).filter_by(id=result.id).first()
        assert fetched_article is not None
        assert fetched_article.title == title
        assert fetched_article.content == content
        assert fetched_article.status == status
        assert fetched_article.author_id == author.id
        assert fetched_article.category_id == (category.id if category else None)
        assert result == fetched_article


@pytest.mark.parametrize(
    "article_data, expected_count",
    [
        ([("Article 1", "Content 1"), ("Article 2", "Content 2")], 2),
        ([], 0),
    ],
)
def test_get_all_articles(db_session, repository, article_data, expected_count):
    author = create_user(db_session)
    category = create_category(db_session)

    for title, content in article_data:
        article = create_article(
            db_session,
            title=title,
            content=content,
            status=ArticleStatus.DRAFT,
            author=author,
            category=category,
        )
        db_session.add(article)

    db_session.commit()

    fetched_articles: List[Articles] = repository.get_all_articles()

    assert fetched_articles is not None
    assert isinstance(fetched_articles, list)
    assert len(fetched_articles) == expected_count

    if expected_count > 0:
        for i, article in enumerate(fetched_articles):
            assert article.title == article_data[i][0]
            assert article.content == article_data[i][1]


@pytest.mark.parametrize(
    "status, expected_count",
    [
        (ArticleStatus.DRAFT, 1),
        (ArticleStatus.PUBLISHED, 1),
        (ArticleStatus.REJECTED, 1),
    ],
)
def test_get_article_by_status(db_session, repository, status, expected_count):

    author = create_user(db_session)
    category = create_category(db_session)
    create_article(
        db_session,
        title="Draft Article 1",
        content="Content 1",
        status=ArticleStatus.DRAFT,
        author=author,
        category=category,
    )
    create_article(
        db_session,
        title="Draft Article 2",
        content="Content 2",
        status=ArticleStatus.PUBLISHED,
        author=author,
        category=category,
    )
    create_article(
        db_session,
        title="Published Article",
        content="Content 3",
        status=ArticleStatus.REJECTED,
        author=author,
        category=category,
    )

    fetched_articles: List[Articles] = repository.get_article_by_status(status)

    assert fetched_articles is not None
    assert isinstance(fetched_articles, list)
    assert len(fetched_articles) == expected_count

    for article in fetched_articles:
        assert article.status == status


@pytest.mark.parametrize(
    "should_create, should_exist",
    [
        (True, True),
        (False, False),
    ],
)
def test_get_article_by_id(db_session, repository, should_create, should_exist):

    article_id = None

    if should_create:
        author = create_user(db_session)
        article = create_article(
            db_session,
            title="Draft Article 1",
            content="Content 1",
            status=ArticleStatus.DRAFT,
            author=author,
            category=None,
        )
        article_id = article.id
    else:
        article_id = uuid4()

    fetched_article = repository.get_article_by_id(article_id)

    if should_exist:
        assert fetched_article is not None
        assert fetched_article.id == article_id
    else:
        assert fetched_article is None


@pytest.mark.parametrize(
    "update_data, expected_title, expected_content, expected_status",
    [
        (
            {"title": "Updated Title"},
            "Updated Title",
            "Test Content",
            ArticleStatus.DRAFT,
        ),
        (
            {"content": "Updated Content"},
            "Test Article",
            "Updated Content",
            ArticleStatus.DRAFT,
        ),
        ({}, "Test Article", "Test Content", ArticleStatus.DRAFT),
    ],
)
def test_update_article(
    db_session,
    repository,
    update_data,
    expected_title,
    expected_content,
    expected_status,
):

    author = create_user(db_session)
    category = create_category(db_session)

    article = create_article(
        db_session,
        title="Test Article",
        content="Test Content",
        status=ArticleStatus.DRAFT,
        author=author,
        category=category,
    )

    print(
        f"Before update: title={article.title}, content={article.content}, status={article.status}"
    )

    article_update = ArticleUpdate(**update_data)
    print(f"Updating article with: {update_data}")

    updated_article = repository.update_article(article, article_update)

    assert updated_article is not None
    assert updated_article.title == expected_title
    assert updated_article.content == expected_content
    assert updated_article.status == expected_status

    fetched_article = db_session.query(Articles).filter_by(id=article.id).first()
    assert fetched_article is not None
    assert fetched_article.title == expected_title
    assert fetched_article.content == expected_content
    assert fetched_article.status == expected_status


def test_update_nonexistent_article(db_session, repository):

    non_existent_article = Articles(
        title="Nonexistent", content="No content", status=ArticleStatus.DRAFT
    )

    article_update = ArticleUpdate(title="Updated Title")

    with pytest.raises(Exception):
        repository.update_article(non_existent_article, article_update)


@pytest.mark.parametrize(
    "initial_status, new_status, should_change",
    [
        (ArticleStatus.DRAFT, ArticleStatus.PUBLISHED, True),
        (ArticleStatus.PUBLISHED, ArticleStatus.IN_REVIEW, True),
        (ArticleStatus.DRAFT, ArticleStatus.DRAFT, False),
    ],
)
def test_update_article_status(
    db_session, repository, initial_status, new_status, should_change
):
    author = create_user(db_session)
    category = create_category(db_session, "Test")
    article = create_article(
        db_session,
        title="Test article",
        content="this is test",
        status=initial_status,
        author=author,
        category=category,
    )

    updated_article = repository.update_article_status(article, new_status)

    assert updated_article is not None
    assert updated_article.id == article.id
    assert updated_article.status == new_status

    if should_change:
        assert updated_article.status != initial_status
    else:
        assert updated_article.status == initial_status


def test_update_status_nonexistent_article(db_session, repository):

    non_existent_article = Articles(
        title="Nonexistent", content="No content", status=ArticleStatus.DRAFT
    )
    with pytest.raises(Exception):
        repository.update_article_status(non_existent_article, ArticleStatus.PUBLISHED)


def test_submit_article(db_session, repository):

    author = create_user(db_session)
    category = create_category(db_session, "Test")
    article = create_article(
        db_session,
        title="Test article",
        content="this is test",
        status=ArticleStatus.DRAFT,
        author=author,
        category=category,
    )

    updated_article = repository.submit_article(article, ArticleStatus.IN_REVIEW)

    assert updated_article is not None
    assert updated_article.id == article.id
    assert updated_article.status == ArticleStatus.IN_REVIEW


def test_delete_article_success(db_session, repository):

    author = create_user(db_session)
    category = create_category(db_session, "Test")
    article = create_article(
        db_session,
        title="Test article",
        content="this is test",
        status=ArticleStatus.DRAFT,
        author=author,
        category=category,
    )

    deleted_article = repository.delete_article(article)

    assert deleted_article is not None
    assert deleted_article.id == article.id

    fetched_article = db_session.query(Articles).filter_by(id=article.id).first()
    assert fetched_article is None


def test_delete_article_not_found(db_session, repository):

    non_existent_article = Articles(
        title="Nonexistent", content="No content", status=ArticleStatus.DRAFT
    )

    with pytest.raises(Exception):
        repository.delete_article(non_existent_article)
