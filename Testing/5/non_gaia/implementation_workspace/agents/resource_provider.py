from crewai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any


class ResourceProviderAgent:
    def __init__(self):
        self.role = "Resource Provider"
        self.goal = "Offer available resources that match resource requests"
        self.backstory = "An agent responsible for providing available resources such as medical supplies, fuel, or equipment to meet transportation and emergency response needs."
        self.tools = []

    def create_agent(self):
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=True,
            allow_delegation=False,
            tools=self.tools,
            max_iter=5,
            memory=True
        )

    def find_available_resources(self, resource_type: str, quantity: int, location: str) -> Dict[str, Any]:
        """Find available resources matching the request"""
        # Simulated resource availability
        available_resources = {
            "medical_supplies": ["bandages", "gloves", "oxygen_tanks"],
            "fuel": ["diesel", "gasoline"],
            "equipment": ["ambulances", "fire_trucks", "rescue_vehicles"]
        }
        
        # Check if resource is available
        if resource_type in available_resources:
            available_items = available_resources[resource_type]
            return {
                "resource_type": resource_type,
                "quantity": quantity,
                "location": location,
                "available_items": available_items,
                "status": "available"
            }
        else:
            return {
                "resource_type": resource_type,
                "quantity": quantity,
                "location": location,
                "available_items": [],
                "status": "not_available"
            }

    def confirm_resource_availability(self, resource_request: Dict[str, Any]) -> Dict[str, Any]:
        """Confirm availability of requested resources"""
        return {
            "request_id": resource_request.get("request_id", "unknown"),
            "status": "confirmed",
            "message": "Resources are confirmed available for delivery"
        }