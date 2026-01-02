"""Request logging middleware.

Logs method, path, status code, and request latency
for every incoming HTTP request.
"""

import time

from fastapi import Request

from backend.app.utils.logger import logger


async def log_requests(request: Request, call_next):
    """Log incoming HTTP requests and their latency.

    Args:
        request: Incoming FastAPI request
        call_next: Next middleware or route handler
    """
    start_time = time.time()

    response = await call_next(request)

    latency_ms = (time.time() - start_time) * 1000

    logger.info(
        "%s %s - status=%s latency=%.2fms",
        request.method,
        request.url.path,
        response.status_code,
        latency_ms,
    )

    return response
