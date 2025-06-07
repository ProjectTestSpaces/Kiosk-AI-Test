from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException, status
from app.core.jwt import verify_access_token

class AdminJWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/admin"):
            token = request.headers.get("Authorization")
            if token and token.startswith("Bearer "):
                token = token.split(" ")[1]
                payload = verify_access_token(token)
                if payload:
                    response = await call_next(request)
                    return response
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing JWT token.")
        response = await call_next(request)
        return response
