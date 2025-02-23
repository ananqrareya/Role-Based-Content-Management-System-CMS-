import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from typing import List
from app.entities.enums import ArticleStatus
from app.entities.schemas.article_schema import ArticleUpdate, ArticleResponse
from app.services.article_service import ArticleService
from app.repositories.tags_repository import TagsRepository
from app.entities.models import Tags, Categories, Articles
from app.entities.models import User

@pytest.fixture
def article_service(mock_db, mock_tags_repository,mock_categories_repository,mock_article_repository):
    service = ArticleService(mock_db)
    service.article_repository = mock_article_repository
    service.categories_repository = mock_categories_repository
    service.tags_repository = mock_tags_repository
    return service


@pytest.mark.parametrize(
    "tag_name, expected_result, expected_exception",
    [
        ("Technology", Tags(name="Technology"), None),
        ("UnknownTag", None, HTTPException),
    ],
)
def test_check_tag_name_with_article(article_service, mock_tags_repository, tag_name, expected_result,
                                     expected_exception):


    mock_tags_repository.get_tag_by_name.return_value = expected_result

    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            article_service.check_tag_name_with_aritcle(tag_name)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Tag '{tag_name}' not found"
    else:
        result = article_service.check_tag_name_with_aritcle(tag_name)
        assert result == expected_result

    mock_tags_repository.get_tag_by_name.assert_called_once_with(tag_name)


@pytest.mark.parametrize(
    "tag_id, expected_result, expected_exception",
    [
        ("123e4567-e89b-12d3-a456-426614174000", Tags(id="123e4567-e89b-12d3-a456-426614174000"), None),

        ("00000000-0000-0000-0000-000000000000", None, HTTPException),
    ],
)
def test_check_tag_id_with_article(article_service, mock_tags_repository, tag_id, expected_result, expected_exception):

    mock_tags_repository.get_tag_by_id.return_value = expected_result

    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            article_service.check_tag_id_with_aritcle(tag_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Tag '{tag_id}' not found"
    else:
        result = article_service.check_tag_id_with_aritcle(tag_id)
        assert result == expected_result

    mock_tags_repository.get_tag_by_id.assert_called_once_with(tag_id)


@pytest.mark.parametrize(
    "category_name, expected_result, expected_exception",
    [
        ("Technology", Categories(name="Technology"), None),
        ("UnknownCategory", None, HTTPException),
    ],
)
def test_check_category_name_with_article(article_service, mock_categories_repository, category_name, expected_result,
                                          expected_exception):



    mock_categories_repository.get_category_by_name.return_value = expected_result

    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            article_service.check_category_name_with_article(category_name)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Category '{category_name}' not found"
    else:
        result = article_service.check_category_name_with_article(category_name)
        assert result == expected_result

    mock_categories_repository.get_category_by_name.assert_called_once_with(category_name)


@pytest.mark.parametrize(
    "category_id, mock_return_value, expected_exception",
    [
        ("123e4567-e89b-12d3-a456-426614174000", Categories(id="123e4567-e89b-12d3-a456-426614174000"), None),

        ("00000000-0000-0000-0000-000000000000", None, HTTPException),
    ],
)
def test_check_category_id_with_article(article_service, mock_categories_repository, category_id, mock_return_value,
                                        expected_exception):



    mock_categories_repository.get_category_by_id.return_value = mock_return_value

    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            article_service.check_category_id_with_article(category_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Category '{category_id}' not found"
    else:
        result = article_service.check_category_id_with_article(category_id)
        assert isinstance(result, Categories)
        assert result.id == category_id

    mock_categories_repository.get_category_by_id.assert_called_once_with(category_id)


@pytest.mark.parametrize(
    "article_data, tag_objects, expected_result",
    [
        (
            {
                "title": "AI in 2025",
                "content": "The future of AI is promising.",
                "author_id": "123e4567-e89b-12d3-a456-426614174000",
                "category_id": "987e6543-e21b-45c6-b321-654321abcdef",
                "tags": ["AI", "Technology"]
            },
            [Tags(name="AI"), Tags(name="Technology")],
            Articles(
                title="AI in 2025",
                content="The future of AI is promising.",
                author_id="123e4567-e89b-12d3-a456-426614174000",
                category_id="987e6543-e21b-45c6-b321-654321abcdef",
                status=ArticleStatus.DRAFT.value,
                tags=[Tags(name="AI"), Tags(name="Technology")]
            ),
        )
    ],
)
def test_create_article(article_service, mock_article_repository, mock_tags_repository, article_data, tag_objects, expected_result):



    mock_tags_repository.get_tag_by_name.side_effect = lambda tag_name: next(
        (tag for tag in tag_objects if tag.name == tag_name), None
    )


    mock_article_repository.add_article.return_value = expected_result


    article_data["tags"] = [mock_tags_repository.get_tag_by_name(tag_name) for tag_name in article_data["tags"]]

    result = article_service.create_article(article_data)


    mock_article_repository.add_article.assert_called_once()


    assert isinstance(result, Articles)
    assert result.title == article_data["title"]
    assert result.content == article_data["content"]
    assert result.author_id == article_data["author_id"]
    assert result.category_id == article_data["category_id"]
    assert result.status == ArticleStatus.DRAFT.value
    assert all(isinstance(tag, Tags) for tag in result.tags)
    assert {tag.name for tag in result.tags} == set([tag.name for tag in tag_objects])


@pytest.mark.parametrize(
    "status, mock_return_value, expected_result",
    [
        (
                None,
                [
                    Articles(title="AI 2025", content="AI advancements", author_id="1", category_id="1",
                             status=ArticleStatus.PUBLISHED),
                    Articles(title="Blockchain", content="Future of Blockchain", author_id="2", category_id="2",
                             status=ArticleStatus.DRAFT)
                ],
                [
                    Articles(title="AI 2025", content="AI advancements", author_id="1", category_id="1",
                             status=ArticleStatus.PUBLISHED),
                    Articles(title="Blockchain", content="Future of Blockchain", author_id="2", category_id="2",
                             status=ArticleStatus.DRAFT)
                ]
        ),
        (
                ArticleStatus.PUBLISHED,
                [
                    Articles(title="AI 2025", content="AI advancements", author_id="1", category_id="1",
                             status=ArticleStatus.PUBLISHED)
                ],
                [
                    Articles(title="AI 2025", content="AI advancements", author_id="1", category_id="1",
                             status=ArticleStatus.PUBLISHED)
                ]
        ),
        (
                ArticleStatus.DRAFT,
                [
                    Articles(title="Blockchain", content="Future of Blockchain", author_id="2", category_id="2",
                             status=ArticleStatus.DRAFT)
                ],
                [
                    Articles(title="Blockchain", content="Future of Blockchain", author_id="2", category_id="2",
                             status=ArticleStatus.DRAFT)
                ]
        ),
        (
                ArticleStatus.PUBLISHED,
                [],
                []
        )
    ],
)
def test_get_articles_by_status(article_service, mock_article_repository, status, mock_return_value, expected_result):


    if status is None:
        mock_article_repository.get_all_articles.return_value = mock_return_value
    else:
        mock_article_repository.get_article_by_status.return_value = mock_return_value

    result = article_service.get_articles_by_status(status)


    if status is None:
        mock_article_repository.get_all_articles.assert_called_once()
    else:
        mock_article_repository.get_article_by_status.assert_called_once_with(status)


    assert isinstance(result, List)
    assert len(result) == len(expected_result)
    for res, exp in zip(result, expected_result):
        assert res.title == exp.title
        assert res.content == exp.content
        assert res.author_id == exp.author_id
        assert res.category_id == exp.category_id
        assert res.status == exp.status


@pytest.mark.parametrize(
    "article_id, mock_return_value, expected_exception",
    [
        (
                UUID("123e4567-e89b-12d3-a456-426614174000"),
                Articles(
                    id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                    title="AI Future",
                    content="Artificial Intelligence in 2025",
                    author_id=UUID("321e6547-e21b-12d3-b456-654321abcdef"),
                    category_id=UUID("987e6543-e21b-45c6-b321-654321abcdef"),
                    status=ArticleStatus.PUBLISHED
                ),
                None
        ),
        (
                UUID("00000000-0000-0000-0000-000000000000"),
                None,
                HTTPException
        )
    ],
)
def test_get_article_by_id(article_service, mock_article_repository, article_id, mock_return_value, expected_exception):


    mock_article_repository.get_article_by_id.return_value = mock_return_value

    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            article_service.get_article_by_id(article_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Article '{article_id}' not found"
    else:
        result = article_service.get_article_by_id(article_id)


        assert isinstance(result, Articles)
        assert result.id == article_id
        assert result.title == mock_return_value.title
        assert result.content == mock_return_value.content
        assert result.author_id == mock_return_value.author_id
        assert result.category_id == mock_return_value.category_id
        assert result.status == mock_return_value.status


    mock_article_repository.get_article_by_id.assert_called_once_with(article_id)

@pytest.mark.parametrize(
    "article_id, existing_article, article_update, updated_article, expected_exception",
    [
        (
            UUID("123e4567-e89b-12d3-a456-426614174000"),
            Articles(
                id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                title="Old Title",
                content="Old Content",
                author_id=UUID("321e6547-e21b-12d3-b456-654321abcdef"),
                category_id=UUID("987e6543-e21b-45c6-b321-654321abcdef"),
                status=ArticleStatus.PUBLISHED
            ),
            ArticleUpdate(
                title="Updated Title",
                content="Updated Content",
                status=ArticleStatus.DRAFT
            ),
            Articles(
                id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                title="Updated Title",
                content="Updated Content",
                author_id=UUID("321e6547-e21b-12d3-b456-654321abcdef"),
                category_id=UUID("987e6543-e21b-45c6-b321-654321abcdef"),
                status=ArticleStatus.DRAFT
            ),
            None
        ),
        (
            UUID("00000000-0000-0000-0000-000000000000"),
            None,
            ArticleUpdate(
                title="New Title",
                content="New Content",
                status=ArticleStatus.PUBLISHED
            ),
            None,
            HTTPException
        )
    ],
)
def test_update_article(
    article_service, mock_article_repository, article_id, existing_article, article_update, updated_article, expected_exception
):


    mock_article_repository.get_article_by_id.return_value = existing_article
    if existing_article:
        mock_article_repository.update_article.return_value = updated_article

    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            article_service.update_article(article_id, article_update)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Article '{article_id}' not found"
    else:
        result = article_service.update_article(article_id, article_update)


        assert isinstance(result, Articles)
        assert result.id == updated_article.id
        assert result.title == updated_article.title
        assert result.content == updated_article.content
        assert result.status == updated_article.status


    mock_article_repository.get_article_by_id.assert_called_once_with(article_id)
    if existing_article:
        mock_article_repository.update_article.assert_called_once_with(existing_article, article_update)

@pytest.mark.parametrize(
    "article_id, existing_article, expected_exception",
    [
        (
            UUID("123e4567-e89b-12d3-a456-426614174000"),
            Articles(
                id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                title="AI Future",
                content="Artificial Intelligence in 2025",
                author_id=UUID("321e6547-e21b-12d3-b456-654321abcdef"),
                category_id=UUID("987e6543-e21b-45c6-b321-654321abcdef"),
                status=ArticleStatus.PUBLISHED
            ),
            None
        ),
        (
            UUID("00000000-0000-0000-0000-000000000000"),
            None,
            HTTPException
        )
    ],
)
def test_delete_article(article_service, mock_article_repository, article_id, existing_article, expected_exception):


    mock_article_repository.get_article_by_id.return_value = existing_article

    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            article_service.delete_article(article_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Article '{article_id}' not found"
    else:
        article_service.delete_article(article_id)


        mock_article_repository.delete_article.assert_called_once_with(existing_article)


    mock_article_repository.get_article_by_id.assert_called_once_with(article_id)

@pytest.mark.parametrize(
    "article_id, existing_article, new_status, updated_article, expected_exception",
    [
        (
            UUID("123e4567-e89b-12d3-a456-426614174000"),
            Articles(
                id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                title="AI Future",
                content="Artificial Intelligence in 2025",
                author_id=UUID("321e6547-e21b-12d3-b456-654321abcdef"),
                category_id=UUID("987e6543-e21b-45c6-b321-654321abcdef"),
                status=ArticleStatus.DRAFT
            ),
            ArticleStatus.PUBLISHED,
            Articles(
                id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                title="AI Future",
                content="Artificial Intelligence in 2025",
                author_id=UUID("321e6547-e21b-12d3-b456-654321abcdef"),
                category_id=UUID("987e6543-e21b-45c6-b321-654321abcdef"),
                status=ArticleStatus.PUBLISHED
            ),
            None
        ),
        (
            UUID("00000000-0000-0000-0000-000000000000"),
            None,
            ArticleStatus.IN_REVIEW,
            None,
            HTTPException
        )
    ],
)
def test_update_article_status(
    article_service, mock_article_repository, article_id, existing_article, new_status, updated_article, expected_exception
):


    mock_article_repository.get_article_by_id.return_value = existing_article
    if existing_article:
        mock_article_repository.update_article_status.return_value = updated_article

    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            article_service.update_article_status(article_id, new_status)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == f"Article '{article_id}' not found"
    else:
        result = article_service.update_article_status(article_id, new_status)


        assert isinstance(result, Articles)
        assert result.id == updated_article.id
        assert result.status == updated_article.status


    mock_article_repository.get_article_by_id.assert_called_once_with(article_id)
    if existing_article:
        mock_article_repository.update_article_status.assert_called_once_with(existing_article, new_status)


