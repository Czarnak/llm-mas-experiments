import agentscope
from agentscope.agents import AgentBase
from agentscope.message import Msg
import numpy as np


class LocalAgent(AgentBase):
    """
    Agent representing a property owner (local)
    """
    
    def __init__(self, name: str, agent_id: str, location: tuple, price: float, size: float, business_type: str):
        super().__init__(name=name, agent_id=agent_id)
        self.location = location  # (latitude, longitude)
        self.price = price  # monthly rent
        self.size = size  # in square meters
        self.business_type = business_type  # type of business that can fit
        self.in_market = False  # whether the local is currently in the market
        self.offer_id = None  # ID of the current offer
        
    def add_to_market(self):
        """
        Add this local to the marketplace
        """
        self.in_market = True
        self.offer_id = f"offer_{np.random.randint(1000, 9999)}"
        return Msg(
            name=self.name,
            content=f"Added local {self.name} to the market with offer ID {self.offer_id}",
            role="system"
        )
        
    def remove_from_market(self):
        """
        Remove this local from the marketplace
        """
        self.in_market = False
        self.offer_id = None
        return Msg(
            name=self.name,
            content=f"Removed local {self.name} from the market",
            role="system"
        )
        
    def withdraw_offer(self):
        """
        Withdraw the current offer
        """
        if self.in_market:
            self.in_market = False
            offer_id = self.offer_id
            self.offer_id = None
            return Msg(
                name=self.name,
                content=f"Withdrew offer {offer_id} for local {self.name}",
                role="system"
            )
        else:
            return Msg(
                name=self.name,
                content=f"Local {self.name} has no active offer to withdraw",
                role="system"
            )
        
    def handle_message(self, message: Msg) -> Msg:
        """
        Handle incoming messages
        """
        if message.content.startswith("Matched with business"):
            return Msg(
                name=self.name,
                content=f"Local {self.name} received match notification. Accepting or rejecting...",
                role="assistant"
            )
        elif message.content.startswith("Business rejected"):
            return Msg(
                name=self.name,
                content=f"Local {self.name} received rejection from business. Will consider other options.",
                role="assistant"
            )
        else:
            return Msg(
                name=self.name,
                content=f"Local {self.name} received message: {message.content}",
                role="assistant"
            )