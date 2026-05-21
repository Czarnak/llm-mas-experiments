import agentscope
from agentscope.agents import AgentBase
from agentscope.message import Msg
import numpy as np


class BusinessAgent(AgentBase):
    """
    Agent representing a business looking for space
    """
    
    def __init__(self, name: str, agent_id: str, location: tuple, required_size: float, business_type: str, max_price: float):
        super().__init__(name=name, agent_id=agent_id)
        self.location = location  # (latitude, longitude)
        self.required_size = required_size  # in square meters
        self.business_type = business_type  # type of business
        self.max_price = max_price  # maximum price they're willing to pay
        self.requirement_id = None  # ID of the requirement
        
    def place_requirement(self):
        """
        Place a requirement for a local
        """
        self.requirement_id = f"req_{np.random.randint(1000, 9999)}"
        return Msg(
            name=self.name,
            content=f"Business {self.name} placed requirement {self.requirement_id} for size {self.required_size}m², type {self.business_type}, max price {self.max_price}",
            role="system"
        )
        
    def withdraw_requirement(self):
        """
        Withdraw the current requirement
        """
        if self.requirement_id:
            req_id = self.requirement_id
            self.requirement_id = None
            return Msg(
                name=self.name,
                content=f"Business {self.name} withdrew requirement {req_id}",
                role="system"
            )
        else:
            return Msg(
                name=self.name,
                content=f"Business {self.name} has no active requirement to withdraw",
                role="system"
            )
        
    def handle_message(self, message: Msg) -> Msg:
        """
        Handle incoming messages
        """
        if message.content.startswith("Matched with local"):
            return Msg(
                name=self.name,
                content=f"Business {self.name} received match notification. Accepting or rejecting...",
                role="assistant"
            )
        elif message.content.startswith("Local rejected"):
            return Msg(
                name=self.name,
                content=f"Business {self.name} received rejection from local. Will consider other options.",
                role="assistant"
            )
        else:
            return Msg(
                name=self.name,
                content=f"Business {self.name} received message: {message.content}",
                role="assistant"
            )