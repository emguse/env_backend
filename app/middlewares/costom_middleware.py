import json
import logging
import logging.config
from pathlib import Path
import yaml


from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


# Load the logging configuration from YAML file
with open(Path(__file__).parent.parent.parent / "logging.conf", "r") as f:
    config = yaml.safe_load(f)
    # Ensure disable_existing_loggers is False
    config["disable_existing_loggers"] = False
    logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


class RemoveDuplicateHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to remove duplicate headers from the incoming requests.

    This middleware checks if there are multiple 'Content-Type' headers in the request.
    If duplicates are found, it retains only the first one to prevent issues with downstream processing.
    """

    async def dispatch(self, request: Request, call_next):
        headers = request.headers.mutablecopy()
        if headers.getlist("content-type"):
            content_type = headers.getlist("content-type")[0]
            headers["content-type"] = content_type

        request._headers = headers

        response = await call_next(request)
        return response


class LogClientIPMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log the client's IP address for each incoming request.

    This middleware extracts the client's IP address from the request and logs it using the 'log_info' function.
    This is useful for tracking where requests are coming from and for debugging purposes.
    """

    async def dispatch(self, request: Request, call_next):
        # post responce
        logger.info(f"Request URL: {request.url}")
        logger.info(f"Received request from {request.client.host}")
        response = await call_next(request)
        # after response
        logger.info(f"Response status: {response.status_code}")
        return response
