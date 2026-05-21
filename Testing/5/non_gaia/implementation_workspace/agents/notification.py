from crewai import Agent
from pydantic import BaseModel
from typing import List, Dict, Any


class NotificationAgent:
    def __init__(self):
        self.role = "Notification Agent"
        self.goal = "Send notifications about transportation changes and updates"
        self.backstory = "An agent responsible for sending notifications to relevant parties about transportation changes, route updates, and other important information."
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

    def send_notification(self, recipient: str, message: str, priority: str = "normal") -> Dict[str, Any]:
        """Send a notification to a recipient"""
        notification = {
            "recipient": recipient,
            "message": message,
            "priority": priority,
            "timestamp": "2023-05-15 14:30:00",
            "status": "sent"
        }
        
        print(f"Notification sent to {recipient}: {message}")
        return notification

    def send_transport_update(self, route_id: str, update_type: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Send a transportation update"""
        update = {
            "route_id": route_id,
            "update_type": update_type,
            "details": details,
            "timestamp": "2023-05-15 14:30:00",
            "status": "sent"
        }
        
        print(f"Transportation update sent for route {route_id}: {update_type}")
        return update

    def send_alert(self, alert_type: str, message: str, recipients: List[str]) -> Dict[str, Any]:
        """Send an alert to multiple recipients"""
        alert = {
            "alert_type": alert_type,
            "message": message,
            "recipients": recipients,
            "timestamp": "2023-05-15 14:30:00",
            "status": "sent"
        }
        
        print(f"Alert sent ({alert_type}): {message}")
        print(f"Recipients: {recipients}")
        return alert