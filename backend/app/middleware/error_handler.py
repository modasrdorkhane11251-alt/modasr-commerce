"""Error handling middleware."""
import logging
import json
from fastapi import Request, status
from starlette.responses import JSONResponse
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)


async def error_handler_middleware(request: Request, call_next):
    """
    Global error handling middleware.
    """
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        request_id = getattr(request.state, "request_id", "unknown")
        
        # Log error with context
        logger.error(
            f"Unhandled exception: {exc}",
            extra={
                "request_id": request_id,
                "path": request.url.path,
                "method": request.method,
                "client": request.client[0] if request.client else "unknown",
            },
            exc_info=True,
        )
        
        # Return generic error response (don't expose stack traces)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal server error",
                "request_id": request_id,
            },
        )
