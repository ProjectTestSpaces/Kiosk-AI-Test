import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("api_performance")

class PerformanceLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Process the request
        response: Response = await call_next(request)

        duration = round((time.time() - start_time) * 1000, 2)  # ms
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "unknown")

        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} - "
            f"{duration}ms | IP: {client_ip} | UA: {user_agent}"
        )
        return response

