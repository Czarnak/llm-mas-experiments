import agentscope
from agentscope.agents import AgentBase
from agentscope.message import Msg
from agentscope.pipelines import Pipeline
import numpy as np


class MarketplaceAgent(AgentBase):
    """
    Agent managing the marketplace and auction system
    """
    
    def __init__(self, name: str, agent_id: str):
        super().__init__(name=name, agent_id=agent_id)
        self.locals = {}  # Dict of locals in the market
        self.businesses = {}  # Dict of businesses with requirements
        self.residents = {}  # Dict of residents with service requests
        self.auctions = {}  # Dict of active auctions
        
    def add_local(self, local_agent):
        """
        Add a local to the marketplace
        """
        self.locals[local_agent.agent_id] = local_agent
        return Msg(
            name=self.name,
            content=f"Added local {local_agent.name} to marketplace",
            role="system"
        )
        
    def remove_local(self, local_agent):
        """
        Remove a local from the marketplace
        """
        if local_agent.agent_id in self.locals:
            del self.locals[local_agent.agent_id]
            return Msg(
                name=self.name,
                content=f"Removed local {local_agent.name} from marketplace",
                role="system"
            )
        else:
            return Msg(
                name=self.name,
                content=f"Local {local_agent.name} not found in marketplace",
                role="system"
            )
        
    def add_business(self, business_agent):
        """
        Add a business to the marketplace
        """
        self.businesses[business_agent.agent_id] = business_agent
        return Msg(
            name=self.name,
            content=f"Added business {business_agent.name} to marketplace",
            role="system"
        )
        
    def add_resident(self, resident_agent):
        """
        Add a resident to the marketplace
        """
        self.residents[resident_agent.agent_id] = resident_agent
        return Msg(
            name=self.name,
            content=f"Added resident {resident_agent.name} to marketplace",
            role="system"
        )
        
    def start_auction(self, business_agent, local_agent):
        """
        Start an auction between a business and a local
        """
        auction_id = f"auction_{np.random.randint(1000, 9999)}"
        self.auctions[auction_id] = {
            "business": business_agent,
            "local": local_agent,
            "status": "active"
        }
        return Msg(
            name=self.name,
            content=f"Started auction {auction_id} between business {business_agent.name} and local {local_agent.name}",
            role="system"
        )
        
    def handle_message(self, message: Msg) -> Msg:
        """
        Handle incoming messages
        """
        return Msg(
            name=self.name,
            content=f"Marketplace received message: {message.content}",
            role="assistant"
        )