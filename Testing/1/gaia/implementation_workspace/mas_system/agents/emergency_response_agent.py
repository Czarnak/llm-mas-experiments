from typing import Dict, Any, Optional
from .base_agent import BaseAgent, AgentMessage


class EmergencyResponseAgent(BaseAgent):
    def __init__(self, agent_id: str, name: str):
        super().__init__(agent_id, name)
        
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        if message.protocol == "HandleEmergency":
            return self._handle_emergency(message)
        else:
            # Handle unknown protocols
            return None
    
    def _handle_emergency(self, message: AgentMessage) -> Optional[AgentMessage]:
        emergency_event = message.content.get("EmergencyEvent")
        if not emergency_event:
            return None
        
        # In a real implementation, this would handle emergency events
        # For now, we'll just return a confirmation
        return AgentMessage(
            sender=self.agent_id,
            receiver=message.sender,
            protocol="ReconfigurationPlan",
            content={"Plan": "Emergency response plan generated"},
            timestamp=0.0
        )
    
    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "roles": ["EmergencyResponseSystem"],
            "protocols": ["HandleEmergency"],
            "permissions": {
                "read": ["EmergencyEvent"],
                "write": ["EmergencyEvent"],
                "consume": ["EmergencyEvent"],
                "produce": ["ReconfigurationPlan"]
            }
        }