from enum import Enum


class ArticleStatus(str, Enum):
    DRAFT = "Draft"
    IN_REVIEW = "In Review"
    PUBLISHED = "Published"
    REJECTED = "Rejected"
