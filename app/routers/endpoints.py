import json
import logging
import logging.config
from pathlib import Path
from typing import Dict, Any
import yaml

from fastapi import APIRouter, Request
from starlette.datastructures import Headers

from app.cruds.cruds import bulk_insert_env_data
from app.models.sensor_models import ReceiveEnv
from app.models.sensor_models import ReceiveEnv, RecieveLog, SensorData


# Load the logging configuration from YAML file
with open(Path(__file__).parent.parent.parent / "logging.conf", "r") as f:
    config = yaml.safe_load(f)
    # Ensure disable_existing_loggers is False
    config["disable_existing_loggers"] = False
    logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/")
async def root() -> Dict[str, str]:
    """
    Handles GET requests to the root endpoint.

    Returns:
        Dict[str, str]: A dictionary containing a greeting message.
    """
    return {"message": "Hello. World!"}


@router.get("/hello")
async def hello() -> Dict[str, str]:
    """
    Handles GET requests to the '/hello' endpoint.

    Returns:
        Dict[str, str]: A dictionary containing a greeting message.
    """
    return {"message": "Hello. World!"}


@router.post("/post-env4")
async def post_env4(env_data: ReceiveEnv) -> Dict[str, Any]:
    logger.debug(env_data)
    new_data = [
        SensorData(
            sensor_id=env_data.sensor_id,
            sensor_type="temperature",
            value=env_data.temperature,
            timestamp=env_data.timestamp,
        ),
        SensorData(
            sensor_id=env_data.sensor_id,
            sensor_type="humidity",
            value=env_data.humidity,
            timestamp=env_data.timestamp,
        ),
        SensorData(
            sensor_id=env_data.sensor_id,
            sensor_type="pressure",
            value=env_data.pressure,
            timestamp=env_data.timestamp,
        ),
    ]
    bulk_insert_env_data(new_data)
    return {"env_data": env_data}


@router.post("/post-log")
async def post_log(received_log: RecieveLog) -> None:
    level = received_log.level
    message = received_log.message
    print(message)
    level = level.upper()
    if level == "DEBUG":
        logger.debug(message)
    elif level == "INFO":
        logger.info(message)
    elif level == "WARNING":
        logger.warning(message)
    elif level == "ERROR":
        logger.error(message)
    elif level == "CRITICAL":
        logger.warning(message)
    else:
        logger.info(message)


@router.post("/post-test")
async def post_test(request: Request) -> Dict[str, Any]:
    """
    Handles a POST request to the '/post-test' endpoint.

    Extracts headers and body from the request, logs them, and returns the body as JSON.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        Dict[str, Any]: A dictionary containing the parsed JSON body.
    """
    header: Headers = request.headers
    body: bytes = await request.body()
    body_json: Dict[str, Any] = json.loads(body)
    logger.info(header)
    logger.info(body_json)
    return {"body": body_json}
