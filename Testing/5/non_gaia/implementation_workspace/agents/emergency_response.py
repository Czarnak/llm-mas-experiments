from crewai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any


class EmergencyResponseAgent:
    def __init__(self):
        self.role = "Emergency Response Agent"
        self.goal = "Handle emergency situations and send special notifications to law enforcement"
        self.backstory = "An agent responsible for handling emergency situations, coordinating with law enforcement, and sending special notifications about critical incidents."
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

    def handle_emergency(self, incident_type: str, location: str, severity: str) -> Dict[str, Any]:
        """Handle an emergency situation"""
        emergency_response = {
            "incident_id": f"emergency_{hash(location) % 10000}",
            "incident_type": incident_type,
            "location": location,
            "severity": severity,
            "timestamp": "2023-05-15 14:30:00",
            "status": "handled"
        }
        
        print(f"Emergency handled: {incident_type} at {location} (Severity: {severity})")
        return emergency_response

    def notify_law_enforcement(self, incident_id: str, message: str) -> Dict[str, Any]:
        """Send special notification to law enforcement"""
        notification = {
            "incident_id": incident_id,
            "recipient": "Law Enforcement",
            "message": message,
            "timestamp": "2023-05-15 14:30:00",
            "status": "sent"
        }
        
        print(f"Law enforcement notification sent: {message}")
        return notification

    def coordinate_response(self, incident_id: str, resources: List[str]) -> Dict[str, Any]:
        """Coordinate emergency response with available resources"""
        coordination = {
            "incident_id": incident_id,
            "resources": resources,
            "status": "coordinated",
            "timestamp": "2023-05-15 14:30:00"
        }
        
        print(f"Emergency response coordinated for incident {incident_id} with resources: {resources}")
        return coordination