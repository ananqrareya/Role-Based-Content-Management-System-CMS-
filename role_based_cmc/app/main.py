from fastapi import FastAPI

import app
from app.routers.auth_routes import router as auth_routes
from app.routers.user_routes import router as user_routes
from app.routers.article_router import router as article_routes
from app.routers.role_routes import router as role_routes

from app.routers.article_comment_router import router as comments_routes
from app.routers.category_router import router as category_routes
from app.routers.tag_router import router as tag_routes


app = FastAPI(
    title="Role-Based Content Management System (CMS)",
    description="An API for managing content with role-based access control.",
)




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
    tags=["Article Management (Admin and Editor: Full CRUD on all articles.)"],
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
