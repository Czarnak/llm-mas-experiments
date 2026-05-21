from typing import Dict, Any, Optional
from .base_agent import BaseAgent, AgentMessage


class FairRotationAgent(BaseAgent):
    def __init__(self, agent_id: str, name: str):
        super().__init__(agent_id, name)
        
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        if message.protocol == "EnsureFairRotation":
            return self._ensure_fair_rotation(message)
        else:
            # Handle unknown protocols
            return None
    
    def _ensure_fair_rotation(self, message: AgentMessage) -> Optional[AgentMessage]:
        rotation_parameters = message.content.get("RotationParameters")
        if not rotation_parameters:
            return None
        
        # In a real implementation, this would implement fair rotation logic
        # For now, we'll just return a confirmation
        return AgentMessage(
            sender=self.agent_id,
            receiver=message.sender,
            protocol="RotationAdjustment",
            content={"Adjustment": "Fair rotation adjustment applied"},
            timestamp=0.0
        )
    
    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "roles": ["FairRotationManager"],
            "protocols": ["EnsureFairRotation"],
            "permissions": {
                "read": ["RotationParameters"],
                "write": ["RotationParameters"],
                "consume": ["RotationParameters"],
                "produce": ["RotationAdjustment"]
            }
        }