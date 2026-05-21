from crewai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any
import datetime


class CalendarAgent:
    def __init__(self):
        self.role = "Calendar"
        self.goal = "Store all important events and appointments"
        self.backstory = "You are the calendar agent that manages all appointments and events for pet health monitoring."
        self.tools = []
        self.appointments = []

    def create_agent(self):
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            tools=self.tools,
            verbose=True,
            allow_delegation=False
        )

    def get_current_schedule(self) -> List[Dict[str, Any]]:
        """Get current schedule from calendar"""
        return self.appointments

    def add_appointment(self, appointment: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new appointment to the calendar"""
        appointment["id"] = len(self.appointments) + 1
        appointment["created_at"] = datetime.datetime.now().isoformat()
        self.appointments.append(appointment)
        return appointment

    def check_conflicts(self, appointment: Dict[str, Any]) -> bool:
        """Check if appointment conflicts with existing ones"""
        # Simple conflict checking - in real system would be more sophisticated
        for existing in self.appointments:
            if existing["datetime"] == appointment["datetime"]:
                return True
        return False
