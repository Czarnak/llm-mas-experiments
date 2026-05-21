from crewai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any


class ResourceRequesterAgent:
    def __init__(self):
        self.role = "Resource Requester"
        self.goal = "Request specific resources needed for transportation and emergency response"
        self.backstory = "An agent responsible for identifying and requesting specific resources such as medical supplies, fuel, or equipment needed for transportation operations and emergency response."
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

    def process_request(self, resource_type: str, quantity: int, location: str, priority: str = "normal") -> Dict[str, Any]:
        """Process a resource request"""
        request_details = {
            "resource_type": resource_type,
            "quantity": quantity,
            "location": location,
            "priority": priority,
            "status": "requested"
        }
        
        print(f"Resource Requested: {resource_type} x{quantity} at {location} (Priority: {priority})")
        return request_details

    def get_request_status(self, request_id: str) -> Dict[str, Any]:
        """Get status of a specific request"""
        return {
            "request_id": request_id,
            "status": "processing",
            "message": "Request is being processed by resource provider agents"
        }