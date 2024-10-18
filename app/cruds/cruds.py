from datetime import datetime
import logging
import logging.config
from pathlib import Path
from typing import List
import yaml

from sqlmodel import Session

from app.db.db import get_db
from app.models.sensor_models import SensorData

# Load the logging configuration from YAML file
with open(Path(__file__).parent.parent.parent / "logging.conf", "r") as f:
    config = yaml.safe_load(f)
    # Ensure disable_existing_loggers is False
    config["disable_existing_loggers"] = False
    logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


engine = get_db()


def insert_env_data(timestamp: datetime, sensor_id: str, sensor_type: str, value: float) -> None:
    """
    Inserts a single sensor data record into the database.

    Args:
        timestamp (datetime): The timestamp of the sensor data.
        sensor_id (str): The ID of the sensor.
        sensor_type (str): The type of the sensor.
        value (float): The sensor's recorded value.

    Returns:
        None
    """
    with Session(engine) as session:
        new_data = SensorData(
            sensor_id=sensor_id,
            sensor_type=sensor_type,
            value=value,
            timestamp=timestamp,
        )
        session.add(new_data)
        session.commit()


def bulk_insert_env_data(data_list: List[SensorData]) -> None:
    """
    Inserts a list of sensor data into the database in bulk.

    Args:
        data_list (List[SensorData]): A list of SensorData objects to insert.

    Returns:
        None
    """
    with Session(engine) as session:
        session.add_all(data_list)
        session.commit()
