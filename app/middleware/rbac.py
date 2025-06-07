from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException, status
from app.core.jwt import verify_access_token
from app.api.auth import get_current_admin_user

class RBACMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/admin"):
            token = request.headers.get("Authorization")
            if token and token.startswith("Bearer "):
                token = token.split(" ")[1]
                payload = verify_access_token(token)
                if payload and payload.get("role") == "mall_admin":
                    return await call_next(request)
                raise HTTPException(status_code=403, detail="Forbidden: Insufficient permissions")
            raise HTTPException(status_code=401, detail="Missing or invalid token")
        return await call_next(request)

from fastapi import Depends

def require_role(required_role: str):
    def role_checker(user=Depends(get_current_admin_user)):
        if user["role"] != required_role:
            raise HTTPException(status_code=403, detail="Forbidden: Insufficient role")
        return user
    return role_checker