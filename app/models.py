from datetime import datetime, timedelta
from typing import Optional

from pydantic import field_validator
from sqlmodel import Field, SQLModel


# Sensor data model
class SensorData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sensor_id: str  # atoms3+env4
    sensor_type: str  # 'temperature', 'humidity', 'pressure'
    value: float
    timestamp: datetime
    reg_datetime: datetime = Field(default_factory=datetime.now)


class ReceiveEnv(SQLModel):
    timestamp: datetime
    sensor_id: str
    temperature: float
    humidity: float
    pressure: float

    @field_validator("timestamp", mode="before")
    def convert_to_datetime(cls, v):
        if isinstance(v, list) and len(v) >= 6:
            return datetime(*v[:6]) - timedelta(hours=-18)  # 年、月、日、時、分、秒を使ってdatetimeに変換
        raise ValueError("Invalid datetime format")
