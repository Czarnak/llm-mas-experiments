from crewai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any


class TrafficMonitorAgent:
    def __init__(self):
        self.role = "Traffic Monitor"
        self.goal = "Monitor traffic conditions and report incidents"
        self.backstory = "An agent responsible for monitoring real-time traffic conditions, identifying incidents, and communicating road blockages and threats to other agents."
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

    def monitor_traffic(self, location: str) -> Dict[str, Any]:
        """Monitor traffic conditions at a specific location"""
        # Simulated traffic monitoring
        traffic_data = {
            "location": location,
            "traffic_conditions": "heavy",
            "incident": "accident",
            "severity": "high",
            "detour_required": True,
            "status": "monitored"
        }
        
        print(f"Traffic monitored at {location}: {traffic_data['incident']} with {traffic_data['severity']} severity")
        return traffic_data

    def report_incident(self, incident_type: str, location: str, severity: str) -> Dict[str, Any]:
        """Report a traffic incident or road blockage"""
        incident_report = {
            "incident_id": f"incident_{hash(location) % 10000}",
            "type": incident_type,
            "location": location,
            "severity": severity,
            "timestamp": "2023-05-15 14:30:00",
            "status": "reported"
        }
        
        print(f"Incident reported: {incident_type} at {location} (Severity: {severity})")
        return incident_report

    def get_traffic_updates(self) -> List[Dict[str, Any]]:
        """Get latest traffic updates"""
        updates = [
            {
                "location": "Main St & 1st Ave",
                "incident": "construction",
                "severity": "medium",
                "estimated_time": "15 minutes delay"
            },
            {
                "location": "Highway 101 Northbound",
                "incident": "accident",
                "severity": "high",
                "estimated_time": "30 minutes delay"
            }
        ]
        
        return updates