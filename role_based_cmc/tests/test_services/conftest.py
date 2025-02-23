from unittest.mock import MagicMock

import pytest

from app.repositories.article_comment_repository import ArticleCommentRepository
from app.repositories.article_repository import ArticleRepository
from app.repositories.categories_repository import CategoriesRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.tags_repository import TagsRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_token_repository import UserTokenRepository


@pytest.fixture
def mock_db():

    db = MagicMock()
    db.query = MagicMock()
    return db


@pytest.fixture
def mock_role_repository():
    return MagicMock(spec=RoleRepository, autospec=True)


@pytest.fixture
def mock_token_repository():
    return MagicMock(spec=UserTokenRepository, autospec=True)


@pytest.fixture
def mock_user_repository():
    return MagicMock(spec=UserRepository, autospec=True)


@pytest.fixture
def mock_categories_repository():
    return MagicMock(spec=CategoriesRepository, autospec=True)


@pytest.fixture
def mock_tags_repository(mock_db):
    return MagicMock(spec=TagsRepository, autospec=True)

@pytest.fixture
def mock_article_repository(mock_db):
    return MagicMock(spec=ArticleRepository,autospec=True)

@pytest.fixture
def mock_article_comment_repository(mock_db):
    return MagicMock(spec=ArticleCommentRepository,autospec=True)
