from typing import List

from fastapi import APIRouter
from app.schemas.permission_schema import Permission

router = APIRouter()


@router.get("/", response_model=List[Permission],
            summary="Get all permissions")
def get_permissions():
    pass
