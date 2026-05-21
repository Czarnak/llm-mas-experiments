from crewai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any


class MasterAgent:
    def __init__(self):
        self.role = "Master"
        self.goal = "Coordinate workflow and take action based on the analyzed data"
        self.backstory = "You are the master agent that coordinates the workflow and makes decisions based on health analysis results. You determine whether to schedule vet appointments or take no action."
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

    def make_decision(self, analysis_result: Dict[str, Any], current_appointments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Make decision based on analysis and current appointments"""
        decision = {
            "action": "do_nothing",
            "reason": "No health concerns detected"
        }
        
        # Check if there are health alerts
        if analysis_result["health_status"] == "concern":
            # Check if there's already an appointment scheduled
            has_appointment = any(
                appt["reason"] == "health_concern" for appt in current_appointments
            )
            
            if not has_appointment:
                decision["action"] = "schedule_appointment"
                decision["reason"] = "Health concerns detected and no appointment scheduled"
            else:
                decision["reason"] = "Health concerns detected but appointment already scheduled"
        
        return decision

    def get_current_appointments(self) -> List[Dict[str, Any]]:
        """Get current appointments from calendar"""
        # In a real system, this would query the calendar
        # For this simulation, returning empty list
        return []
