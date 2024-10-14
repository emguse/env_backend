from datetime import datetime

from sqlmodel import Session

from db import get_db
from models import SensorData

engine = get_db()


def insert_env_data(timestamp: datetime, sensor_id: str, sensor_type: str, value: float):
    with Session(engine) as session:
        new_data = SensorData(
            sensor_id=sensor_id,
            sensor_type=sensor_type,
            value=value,
            timestamp=timestamp,
        )
        session.add(new_data)
        session.commit()
