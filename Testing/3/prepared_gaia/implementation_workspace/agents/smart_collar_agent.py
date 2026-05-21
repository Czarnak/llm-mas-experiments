from crewai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any


class SmartCollarAgent:
    def __init__(self):
        self.role = "Data Aggregator and Parser"
        self.goal = "Aggregate raw data from different sensors and parse it into a useful form"
        self.backstory = "You are a smart collar agent that aggregates data from multiple sensors and parses it into a structured format for further analysis."
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

    def aggregate_data(self, raw_data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate raw sensor data from multiple sources"""
        # Simple aggregation - in a real system, this would be more sophisticated
        aggregated = {
            "timestamp": raw_data_list[0]["timestamp"] if raw_data_list else None,
            "sensor_data": raw_data_list,
            "averages": {
                "temperature": sum([d["temperature"] for d in raw_data_list]) / len(raw_data_list) if raw_data_list else 0,
                "heart_rate": sum([d["heart_rate"] for d in raw_data_list]) / len(raw_data_list) if raw_data_list else 0,
                "activity_level": sum([d["activity_level"] for d in raw_data_list]) / len(raw_data_list) if raw_data_list else 0,
                "battery_level": sum([d["battery_level"] for d in raw_data_list]) / len(raw_data_list) if raw_data_list else 0,
                "steps": sum([d["steps"] for d in raw_data_list]) / len(raw_data_list) if raw_data_list else 0,
                "sleep_duration": sum([d["sleep_duration"] for d in raw_data_list]) / len(raw_data_list) if raw_data_list else 0,
            }
        }
        return aggregated

    def parse_data(self, aggregated_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse aggregated data into structured format"""
        parsed = {
            "timestamp": aggregated_data["timestamp"],
            "metrics": {
                "temperature": aggregated_data["averages"]["temperature"],
                "heart_rate": aggregated_data["averages"]["heart_rate"],
                "activity_level": aggregated_data["averages"]["activity_level"],
                "battery_level": aggregated_data["averages"]["battery_level"],
                "steps": aggregated_data["averages"]["steps"],
                "sleep_duration": aggregated_data["averages"]["sleep_duration"],
            },
            "location": {
                "latitude": aggregated_data["sensor_data"][0]["location"]["latitude"] if aggregated_data["sensor_data"] else 0,
                "longitude": aggregated_data["sensor_data"][0]["location"]["longitude"] if aggregated_data["sensor_data"] else 0
            }
        }
        return parsed
