import agentscope
from agentscope.agents import AgentBase
from agentscope.message import Msg
import numpy as np


class MatchingEngineAgent(AgentBase):
    """
    Agent responsible for matching locals with businesses based on criteria
    """
    
    def __init__(self, name: str, agent_id: str, min_price: float = 0, max_price: float = 10000,
                 min_size: float = 0, max_size: float = 1000):
        super().__init__(name=name, agent_id=agent_id)
        self.min_price = min_price
        self.max_price = max_price
        self.min_size = min_size
        self.max_size = max_size
        
    def set_criteria_bounds(self, min_price: float, max_price: float, min_size: float, max_size: float):
        """
        Set the bounds for matching criteria
        """
        self.min_price = min_price
        self.max_price = max_price
        self.min_size = min_size
        self.max_size = max_size
        return Msg(
            name=self.name,
            content=f"Updated matching criteria bounds: price({min_price}-{max_price}), size({min_size}-{max_size})",
            role="system"
        )
        
    def calculate_match_score(self, business_agent, local_agent):
        """
        Calculate a match score based on criteria
        """
        # Location distance (simplified)
        location_distance = np.sqrt((business_agent.location[0] - local_agent.location[0])**2 + 
                                   (business_agent.location[1] - local_agent.location[1])**2)
        
        # Price match (normalized)
        price_match = 1.0 - min(1.0, abs(business_agent.max_price - local_agent.price) / business_agent.max_price)
        
        # Size match (normalized)
        size_match = 1.0 - min(1.0, abs(business_agent.required_size - local_agent.size) / business_agent.required_size)
        
        # Business type match (exact match)
        business_type_match = 1.0 if business_agent.business_type == local_agent.business_type else 0.0
        
        # Calculate weighted score (location has less weight)
        score = (0.3 * price_match + 0.3 * size_match + 0.3 * business_type_match + 0.1 * (1 - location_distance))
        
        return score
        
    def find_matches(self, business_agent, marketplace_agent):
        """
        Find matching locals for a business
        """
        matches = []
        
        for local_id, local_agent in marketplace_agent.locals.items():
            # Check if local meets criteria
            if (self.min_price <= local_agent.price <= self.max_price and
                self.min_size <= local_agent.size <= self.max_size and
                business_agent.business_type == local_agent.business_type):
                
                score = self.calculate_match_score(business_agent, local_agent)
                matches.append((local_agent, score))
                
        # Sort by score (descending)
        matches.sort(key=lambda x: x[1], reverse=True)
        
        return matches
        
    def handle_message(self, message: Msg) -> Msg:
        """
        Handle incoming messages
        """
        return Msg(
            name=self.name,
            content=f"Matching engine received message: {message.content}",
            role="assistant"
        )