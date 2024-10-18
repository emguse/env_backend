import json
import logging
import logging.config
from pathlib import Path
import yaml

from fastapi import FastAPI
import uvicorn

from app.config.config import BaseConfig
from app.db.db import create_tables
from app.middlewares.costom_middleware import RemoveDuplicateHeadersMiddleware, LogClientIPMiddleware
from app.routers import endpoints

# Load the logging configuration from YAML file
with open(Path(__file__).parent.parent / "logging.conf", "r") as f:
    config = yaml.safe_load(f)
    # Ensure disable_existing_loggers is False
    config["disable_existing_loggers"] = False
    logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

config = BaseConfig()


app = FastAPI(title=config.PROJECT_NAME)
# add middlewares
app.add_middleware(RemoveDuplicateHeadersMiddleware)
app.add_middleware(LogClientIPMiddleware)
# add router
app.include_router(endpoints.router)

create_tables()
logger.info("Initialization complete")


if __name__ == "__main__":
    create_tables()
    logger.info("attempt start server")
    uvicorn.run(app, host="0.0.0.0", port=8000)
