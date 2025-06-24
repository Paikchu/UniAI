"""Exception handling middleware"""
import logging

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from core.exceptions import UniAIException
from utils.time_utils import get_current_timestamp

logger = logging.getLogger(__name__)


async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Unified exception handler"""

    # Get request ID (if exists)
    request_id = getattr(request.state, 'request_id', 'unknown')

    if isinstance(exc, UniAIException):
        # Custom exception
        logger.warning(f"UniAI Exception: {exc.message}")
        return JSONResponse(
            status_code=exc.code,
            content={
                "code": exc.code,
                "message": exc.message,
                "request_id": request_id,
                "timestamp": get_current_timestamp()
            }
        )

    elif isinstance(exc, HTTPException):
        # FastAPI HTTP exception
        logger.warning(f"HTTP Exception: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": exc.detail,
                "request_id": request_id,
                "timestamp": get_current_timestamp()
            }
        )

    else:
        # Unknown exception
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "message": "Internal server error",
                "request_id": request_id,
                "timestamp": get_current_timestamp()
            }
        )
