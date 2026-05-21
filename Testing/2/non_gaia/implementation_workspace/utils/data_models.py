from pydantic import BaseModel
from typing import List
from datetime import datetime


class SensorData(BaseModel):
    sensor_id: str
    location: str
    timestamp: datetime
    rat_count: int


class AlertData(BaseModel):
    location: str
    timestamp: datetime
    rat_count: int
    severity: str  # 'low', 'medium', 'high'
    affected_areas: List[str]


class NotificationData(BaseModel):
    room_id: str
    location: str
    timestamp: datetime
    status: str  # 'safe', 'warning', 'critical'
    message: str