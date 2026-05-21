from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class AgentMessage:
    sender: str
    receiver: str
    protocol: str
    content: Dict[str, Any]
    timestamp: float

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "protocol": self.protocol,
            "content": self.content,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            sender=data["sender"],
            receiver=data["receiver"],
            protocol=data["protocol"],
            content=data["content"],
            timestamp=data["timestamp"]
        )


class BaseAgent(ABC):
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.message_queue = []
        
    @abstractmethod
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        pass
    
    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        pass
    
    def send_message(self, receiver_id: str, protocol: str, content: Dict[str, Any]) -> AgentMessage:
        message = AgentMessage(
            sender=self.agent_id,
            receiver=receiver_id,
            protocol=protocol,
            content=content,
            timestamp=0.0  # This would be set by the messaging system
        )
        return message
    
    def add_to_queue(self, message: AgentMessage):
        self.message_queue.append(message)
        
    def process_queue(self):
        while self.message_queue:
            message = self.message_queue.pop(0)
            response = self.process_message(message)
            if response:
                # In a real system, this would send the response back
                pass