from fastapi import FastAPI
from fastapi.params import Depends

import app
from app.core.database import get_db
from app.routers.auth_router import router as auth_routes
from app.routers.user_router import router as user_routes
from app.routers.article_router import router as article_routes
from app.routers.role_router import router as role_routes

from app.routers.article_comment_router import router as comments_routes
from app.routers.category_router import router as category_routes
from app.routers.tag_router import router as tag_routes
from app.routers.author_router import router as author_routes
from app.routers.reader_router import router as reader_routes
from app.utils.fastapi.middleware import JWTMiddleware

PUBLIC_PATHS = [
    "/",
    "/api/auth/login",
    "/api/users/register",
    "/docs",
    "/openapi.json",
]


app = FastAPI(
    title="Role-Based Content Management System (CMS)",
    description="An API for managing content with role-based access control.",
)


app.add_middleware(JWTMiddleware, public_paths=PUBLIC_PATHS)



app.include_router(auth_routes, prefix="/api/auth", tags=["Authorization"])
app.include_router(user_routes, prefix="/api/users", tags=["User Management"])
app.include_router(
    role_routes,
    prefix="/api/roles",
    tags=["Role Management (Admins Only)"],

)

app.include_router(
    article_routes,
    prefix="/api/articles",
    tags=["Article Management (Full CRUD on all articles.)"],
)
app.include_router(
    author_routes,
    prefix="/api/authors",
    tags=["Author"],
)
app.include_router(
    reader_routes,
    prefix="/api/readers",
    tags=["Reader"],
)
app.include_router(comments_routes, prefix="/api/comments", tags=["Comments"])
app.include_router(
    category_routes, prefix="/api/categories",
    tags=["Category Management APIs"]
)

app.include_router(tag_routes, prefix="/api/tags",
                   tags=["Tag Management APIs"])


@app.get("/")
def read_root():
    return {"message": "Welcome to CMS!"}
