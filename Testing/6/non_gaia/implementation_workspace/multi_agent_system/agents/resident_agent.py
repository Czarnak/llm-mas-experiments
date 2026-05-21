import agentscope
from agentscope.agents import AgentBase
from agentscope.message import Msg
import numpy as np


class ResidentAgent(AgentBase):
    """
    Agent representing a resident who wants services
    """
    
    def __init__(self, name: str, agent_id: str, location: tuple):
        super().__init__(name=name, agent_id=agent_id)
        self.location = location  # (latitude, longitude)
        self.service_request_id = None  # ID of the service request
        
    def place_service_request(self, service_type: str):
        """
        Place a service request
        """
        self.service_request_id = f"sr_{np.random.randint(1000, 9999)}"
        return Msg(
            name=self.name,
            content=f"Resident {self.name} placed service request {self.service_request_id} for {service_type}",
            role="system"
        )
        
    def withdraw_service_request(self):
        """
        Withdraw the current service request
        """
        if self.service_request_id:
            sr_id = self.service_request_id
            self.service_request_id = None
            return Msg(
                name=self.name,
                content=f"Resident {self.name} withdrew service request {sr_id}",
                role="system"
            )
        else:
            return Msg(
                name=self.name,
                content=f"Resident {self.name} has no active service request to withdraw",
                role="system"
            )
        
    def handle_message(self, message: Msg) -> Msg:
        """
        Handle incoming messages
        """
        if message.content.startswith("Service request matched"):
            return Msg(
                name=self.name,
                content=f"Resident {self.name} received service request match notification.",
                role="assistant"
            )
        else:
            return Msg(
                name=self.name,
                content=f"Resident {self.name} received message: {message.content}",
                role="assistant"
            )