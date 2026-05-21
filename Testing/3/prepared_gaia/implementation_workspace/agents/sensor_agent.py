from crewai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any


class SensorAgent:
    def __init__(self):
        self.role = "Sensor Simulator"
        self.goal = "Generate realistic raw data like a sensor"
        self.backstory = "You are a sensor simulator that generates realistic raw data for pet monitoring purposes. You produce data that mimics real-world sensor readings."
        self.tools = []

    def create_agent(self):
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            tools=self.tools,
            verbose=True,
            allow_delegation=False
        )

    def generate_sensor_data(self) -> Dict[str, Any]:
        """Generate realistic sensor data for pet monitoring"""
        import random
        import datetime
        
        # Simulate different types of sensor data
        data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "temperature": round(random.uniform(38.0, 40.0), 2),  # Body temperature in Celsius
            "heart_rate": random.randint(60, 120),  # Beats per minute
            "activity_level": random.randint(0, 100),  # Activity level percentage
            "location": {
                "latitude": round(random.uniform(52.0, 53.0), 6),
                "longitude": round(random.uniform(13.0, 14.0), 6)
            },
            "battery_level": random.randint(20, 100),  # Battery percentage
            "steps": random.randint(0, 5000),  # Steps walked
            "sleep_duration": random.randint(0, 12),  # Hours of sleep
        }
        
        return data
