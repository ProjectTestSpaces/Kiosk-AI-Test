from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
# import logging
from app.logger import logger

# # Set up basic logging config (can be enhanced later)
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
# logger = logging.getLogger("admin_logger")


class AdminLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/admin"):
            body = await request.body()
            logger.info(
                f"Admin Request: {request.method} {request.url.path} | Headers: {dict(request.headers)} | Body: {body.decode('utf-8')}"
            )
        response = await call_next(request)
        return response
