
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException

from app.core.database import get_db
from app.services.user_token_service import UserTokenService
from app.utils.auth_utils import verify_access_token


class JWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, public_paths: list[str] = None):
        self.public_paths = public_paths or []
        super().__init__(app)
    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.public_paths:
            return await call_next(request)
        try:
            db = next(get_db())
            user_token_service = UserTokenService(db=db)
            payload = verify_access_token(request, user_token_service)
            request.state.user = payload
            response = await call_next(request)

            return response
        except HTTPException as exc:
            return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)
        except Exception as exc:
            return JSONResponse(content={"detail": f"Error: {str(exc)}"}, status_code=500)