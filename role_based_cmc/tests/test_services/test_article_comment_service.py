from unittest.mock import MagicMock

import pytest
from uuid import UUID

from app.entities.models import Comments, Articles, User
from app.services.article_comment_service import ArticleCommentService
from app.services.article_service import ArticleService


@pytest.fixture
def mock_article_service(mock_db):
    return MagicMock(spec=ArticleService)

@pytest.fixture
def article_comment_service(mock_db, mock_article_comment_repository, mock_article_service):
    service = ArticleCommentService(mock_db)
    service.article_comment_repository = mock_article_comment_repository
    service.article_service = mock_article_service
    return service

@pytest.mark.parametrize(
    "article_id, comment, user_id, existing_article, expected_result, expected_exception",
    [
        (
            UUID("123e4567-e89b-12d3-a456-426614174000"),
            "Great article!",
            "321e6547-e21b-12d3-b456-654321abcdef",
            Articles(id=UUID("123e4567-e89b-12d3-a456-426614174000")),
            Comments(
                article_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                user_id=UUID("321e6547-e21b-12d3-b456-654321abcdef"),
                content="Great article!",
            ),
            None
        ),
        (
            UUID("00000000-0000-0000-0000-000000000000"),
            "Nice read!",
            "321e6547-e21b-12d3-b456-654321abcdef",
            None,
            None,
            ValueError
        ),
    ],
)
def test_new_comment(
    article_comment_service, mock_article_comment_repository, mock_article_service,
    article_id, comment, user_id, existing_article, expected_result, expected_exception
):


    mock_article_service.get_article_by_id.return_value = existing_article
    if existing_article:
        mock_article_comment_repository.save_comment.return_value = expected_result

    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            article_comment_service.new_comment(article_id, comment, user_id)

        assert str(exc_info.value) == f"article with id {article_id} does not exist"
    else:
        result = article_comment_service.new_comment(article_id, comment, user_id)


        assert isinstance(result, Comments)
        assert result.article_id == expected_result.article_id
        assert result.user_id == expected_result.user_id
        assert result.content == expected_result.content


    mock_article_service.get_article_by_id.assert_called_once_with(article_id)
    if existing_article:
        mock_article_comment_repository.save_comment.assert_called_once()

@pytest.mark.parametrize(
    "article_id, existing_article, expected_result, expected_exception",
    [
        (
            UUID("123e4567-e89b-12d3-a456-426614174000"),
            Articles(
                id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                title="AI Future",
                content="Artificial Intelligence in 2025",
                comments=[
                    Comments(id=UUID("111e6547-e21b-12d3-b456-654321abcdef"), content="Great article!", user=User(username="JohnDoe")),
                    Comments(id=UUID("222e6547-e21b-12d3-b456-654321abcdef"), content="Interesting read!", user=User(username="JaneDoe")),
                ]
            ),
            Articles(
                id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                title="AI Future",
                content="Artificial Intelligence in 2025",
                comments=[
                    Comments(id=UUID("111e6547-e21b-12d3-b456-654321abcdef"), content="Great article!", user=User(username="JohnDoe")),
                    Comments(id=UUID("222e6547-e21b-12d3-b456-654321abcdef"), content="Interesting read!", user=User(username="JaneDoe")),
                ]
            ),
            None
        ),
        (
            UUID("00000000-0000-0000-0000-000000000000"),
            None,
            None,
            ValueError
        ),
    ],
)
def test_get_article_with_comment(
    article_comment_service, mock_article_service, article_id, existing_article, expected_result, expected_exception
):


    mock_article_service.get_article_by_id.return_value = existing_article

    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            article_comment_service.get_article_with_comment(article_id)

        assert str(exc_info.value) == f"article with id {article_id} does not exist"
    else:
        result = article_comment_service.get_article_with_comment(article_id)


        assert isinstance(result, Articles)
        assert result.id == expected_result.id
        assert result.title == expected_result.title
        assert result.content == expected_result.content
        assert len(result.comments) == len(expected_result.comments)


        for res_comment, exp_comment in zip(result.comments, expected_result.comments):
            assert res_comment.content == exp_comment.content
            assert res_comment.user.username == exp_comment.user.username


    mock_article_service.get_article_by_id.assert_called_once_with(article_id)

@pytest.mark.parametrize(
    "comment_id, new_comment_text, existing_comment, expected_result, expected_exception",
    [
        (
            UUID("123e4567-e89b-12d3-a456-426614174000"),
            "Updated comment text",
            Comments(
                id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                content="Original comment",
                user=User(username="JohnDoe")
            ),
            Comments(
                id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                content="Updated comment text",
                user=User(username="JohnDoe")
            ),
            None
        ),
        (
            UUID("00000000-0000-0000-0000-000000000000"),
            "New comment text",
            None,
            None,
            ValueError
        ),
    ],
)
def test_update_comment(
    article_comment_service, mock_article_comment_repository, comment_id, new_comment_text,
    existing_comment, expected_result, expected_exception
):


    mock_article_comment_repository.get_comment_by_id.return_value = existing_comment
    if existing_comment:
        mock_article_comment_repository.update_comment.return_value = expected_result

    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            article_comment_service.update_comment(comment_id, new_comment_text)

        assert str(exc_info.value) == f"comment with id {comment_id} does not exist"
    else:
        result = article_comment_service.update_comment(comment_id, new_comment_text)


        assert isinstance(result, Comments)
        assert result.id == expected_result.id
        assert result.content == expected_result.content


    mock_article_comment_repository.get_comment_by_id.assert_called_once_with(comment_id)
    if existing_comment:
        mock_article_comment_repository.update_comment.assert_called_once_with(existing_comment, new_comment_text)

@pytest.mark.parametrize(
    "comment_id, existing_comment, expected_exception",
    [
        (
            UUID("123e4567-e89b-12d3-a456-426614174000"),
            Comments(
                id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                content="This is a comment",
                user=User(username="JohnDoe")
            ),
            None
        ),
        (
            UUID("00000000-0000-0000-0000-000000000000"),
            None,
            ValueError
        ),
    ],
)
def test_delete_comment(
    article_comment_service, mock_article_comment_repository, comment_id,
    existing_comment, expected_exception
):


    mock_article_comment_repository.get_comment_by_id.return_value = existing_comment

    if expected_exception:
        with pytest.raises(expected_exception) as exc_info:
            article_comment_service.delete_comment(comment_id)

        assert str(exc_info.value) == f"comment with id {comment_id} does not exist"
    else:
        result = article_comment_service.delete_comment(comment_id)


        assert isinstance(result, Comments)
        assert result.id == existing_comment.id
        assert result.content == existing_comment.content


    mock_article_comment_repository.get_comment_by_id.assert_called_once_with(comment_id)
    if existing_comment:
        mock_article_comment_repository.delete_comment.assert_called_once_with(existing_comment)
