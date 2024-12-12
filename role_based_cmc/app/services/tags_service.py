from app.entities.schemas.tag_schema import TagCreate
from app.repositories.tags_repository import TagsRepository
from app.entities.models.Tags import Tags
from uuid import UUID
class TagsService:
    def __init__(self, tags_repository: TagsRepository):
        self.tags_repository = tags_repository

    def create_tag(self, tag: TagCreate):
        if self.tags_repository.get_tag_by_name(tag.name):
            raise ValueError(f'Tag {tag.name} already exists')
        tag_db=Tags(
            name=tag.name,
        )
        return self.tags_repository.add_tag(tag_db)
    def get_all_tags(self):
        return self.tags_repository.get_all_tags()

    def delete_tag(self, tag_id:UUID):
        tag_db=self.tags_repository.get_tag_by_id(tag_id)
        if tag_db is None:
            raise ValueError(f'Tag {tag_id} does not exist')
        self.tags_repository.delete_tag(tag_db)
        return tag_db