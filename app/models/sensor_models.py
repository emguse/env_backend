from datetime import datetime
from typing import Optional

from pydantic import field_validator
from sqlmodel import Field, SQLModel


# Sensor data model
class SensorData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sensor_id: str  # atoms3+env4
    sensor_type: str  # 'temperature', 'humidity', 'pressure'
    value: float
    timestamp: datetime = Field(index=True)
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
            return datetime(*v[:6])
        raise ValueError("Invalid datetime format")


class RecieveLog(SQLModel):
    level: str
    message: str
