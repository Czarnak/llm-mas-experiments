from pydantic import BaseModel
from typing import List
import random
from datetime import datetime

class SensorData(BaseModel):
    sensor_id: str
    location: str
    timestamp: datetime
    rat_count: int
    

class SensorAgent:
    def __init__(self, sensor_id: str, location: str):
        self.sensor_id = sensor_id
        self.location = location
    
    def generate_data(self) -> SensorData:
        # Simulate sensor data generation
        # In a real system, this would interface with actual sensors
        rat_count = random.randint(0, 10)  # Random rat count for simulation
        
        return SensorData(
            sensor_id=self.sensor_id,
            location=self.location,
            timestamp=datetime.now(),
            rat_count=rat_count
        )