from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import traceback
import uuid
from typing import Dict, Any
import asyncio
from sqlalchemy.exc import SQLAlchemyError
from jwt import PyJWTError
import json

logger = logging.getLogger("app")

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, debug: bool = False):
        super().__init__(app)
        self.debug = debug
    
    async def dispatch(self, request: Request, call_next):
        error_id = str(uuid.uuid4())[:8]  # Short error ID for tracking
        
        try:
            response = await call_next(request)
            return response
            
        except RequestValidationError as exc:
            logger.warning(
                f"Validation error [{error_id}]: {exc} | Path: {request.url.path} | Method: {request.method}"
            )
            return self._create_validation_error_response(exc, error_id)
            
        except StarletteHTTPException as exc:
            logger.warning(
                f"HTTP exception [{error_id}]: {exc.detail} | Status: {exc.status_code} | Path: {request.url.path}"
            )
            return self._create_http_error_response(exc, error_id)
            
        except PyJWTError as exc:
            logger.warning(f"JWT error [{error_id}]: {exc}")
            return self._create_auth_error_response(error_id)
            
        except SQLAlchemyError as exc:
            logger.error(f"Database error [{error_id}]: {exc}")
            return self._create_database_error_response(error_id)
            
        except asyncio.TimeoutError:
            logger.error(f"Timeout error [{error_id}]: Request timeout")
            return self._create_timeout_error_response(error_id)
            
        except PermissionError as exc:
            logger.warning(f"Permission error [{error_id}]: {exc}")
            return self._create_permission_error_response(error_id)
            
        except ValueError as exc:
            logger.error(f"Value error [{error_id}]: {exc}")
            return self._create_value_error_response(exc, error_id)
            
        except Exception as exc:
            logger.exception(f"Unhandled error [{error_id}]: {type(exc).__name__}: {exc}")
            return self._create_internal_error_response(exc, error_id)
    
    def _create_validation_error_response(self, exc: RequestValidationError, error_id: str) -> JSONResponse:
        """Create response for validation errors with detailed field information"""
        errors = []
        for error in exc.errors():
            field_path = " -> ".join(str(loc) for loc in error["loc"])
            errors.append({
                "field": field_path,
                "message": error["msg"],
                "type": error["type"]
            })
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Validation Error",
                "message": "Request validation failed",
                "details": errors,
                "error_id": error_id
            }
        )
    
    def _create_http_error_response(self, exc: StarletteHTTPException, error_id: str) -> JSONResponse:
        """Create response for HTTP exceptions"""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "HTTP Error",
                "message": exc.detail,
                "error_id": error_id
            }
        )
    
    def _create_auth_error_response(self, error_id: str) -> JSONResponse:
        """Create response for authentication errors"""
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": "Authentication Error",
                "message": "Invalid or expired authentication token",
                "error_id": error_id
            }
        )
    
    def _create_database_error_response(self, error_id: str) -> JSONResponse:
        """Create response for database errors"""
        
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": "Database Error",
                "message": "Database operation failed. Please try again later.",
                "error_id": error_id
            }
        )
    
    def _create_timeout_error_response(self, error_id: str) -> JSONResponse:
        """Create response for timeout errors"""
        return JSONResponse(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            content={
                "error": "Timeout Error",
                "message": "Request timed out. Please try again.",
                "error_id": error_id
            }
        )
    
    def _create_permission_error_response(self, error_id: str) -> JSONResponse:
        """Create response for permission errors"""
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "error": "Permission Denied",
                "message": "You don't have permission to access this resource",
                "error_id": error_id
            }
        )
    
    def _create_value_error_response(self, exc: ValueError, error_id: str) -> JSONResponse:
        """Create response for value errors"""
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "Invalid Value",
                "message": str(exc) if self.debug else "Invalid input provided",
                "error_id": error_id
            }
        )
    
    def _create_internal_error_response(self, exc: Exception, error_id: str) -> JSONResponse:
        print("Somewhere here")
        """Create response for internal server errors"""
        content = {
            "error": f"Internal Server Error{exc}",
            "message": "An unexpected error occurred. Please contact support if the problem persists.",
            "error_id": error_id
        }
        
        # Include debug information only in debug mode
        if self.debug:
            content["debug"] = {
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
                "traceback": traceback.format_exc()
            }
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            
            content=content
        )


# Custom exception classes for your application
class BusinessLogicError(Exception):
    """Custom exception for business logic errors"""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(message)


class ResourceNotFoundError(Exception):
    """Custom exception for resource not found errors"""
    def __init__(self, resource: str, identifier: str = None):
        self.resource = resource
        self.identifier = identifier
        message = f"{resource} not found"
        if identifier:
            message += f" with identifier: {identifier}"
        super().__init__(message)


class RateLimitError(Exception):
    """Custom exception for rate limiting"""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message)


# Enhanced error handler that also handles custom exceptions
class EnhancedErrorHandlerMiddleware(ErrorHandlerMiddleware):
    async def dispatch(self, request: Request, call_next):
        error_id = str(uuid.uuid4())[:8]
        
        try:
            response = await call_next(request)
            return response
            
        except BusinessLogicError as exc:
            logger.warning(f"Business logic error [{error_id}]: {exc.message}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "Business Logic Error",
                    "message": exc.message,
                    "error_code": exc.error_code,
                    "error_id": error_id
                }
            )
            
        except ResourceNotFoundError as exc:
            logger.info(f"Resource not found [{error_id}]: {exc}")
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "error": "Resource Not Found",
                    "message": str(exc),
                    "error_id": error_id
                }
            )
            
        except RateLimitError as exc:
            logger.warning(f"Rate limit exceeded [{error_id}]: {exc}")
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Rate Limit Exceeded",
                    "message": str(exc),
                    "error_id": error_id
                }
            )
            
        except Exception as exc:
            # Fall back to parent class handling
            return await super().dispatch(request, call_next)