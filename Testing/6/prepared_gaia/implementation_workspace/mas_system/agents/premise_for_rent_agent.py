from .base_agent import BaseAgent
from mas_system.protocols.premise_offer_protocol import PremiseOfferProtocol
from mas_system.protocols.decision_protocol import DecisionProtocol
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from typing import Dict, Any


class PremiseForRentBehaviour(CyclicBehaviour):
    """
    Behaviour for PremiseForRent agent
    """
    
    async def run(self):
        # This is a simplified version - in a real system, this would handle
        # receiving messages and responding appropriately
        msg = await self.receive(timeout=10)
        if msg:
            print(f"PremiseForRent received: {msg.body}")
            # Process the message
            protocol = self.agent.get_protocol("PremiseOffer")
            if protocol:
                result = protocol.process_message(eval(msg.body))
                if result:
                    # Send response
                    response = Message(to=msg.sender, body=str(result))
                    response.set_metadata("protocol", "PremiseOffer")
                    await self.send(response)


class PremiseForRentAgent(BaseAgent):
    """
    Agent representing a premise for rent
    """
    
    def __init__(self, jid: str, password: str, agent_name: str):
        super().__init__(jid, password, agent_name)
        self.premise_id = None
        self.location = None
        self.price = None
        self.size = None
        self.business_type = None
        
    async def setup(self):
        await super().setup()
        
        # Add protocols
        premise_protocol = PremiseOfferProtocol()
        self.add_protocol("PremiseOffer", premise_protocol)
        
        decision_protocol = DecisionProtocol()
        self.add_protocol("DecideOffer", decision_protocol)
        
        # Add behaviours
        behaviour = PremiseForRentBehaviour()
        self.add_behaviour(behaviour)
        
    def set_premise_details(self, premise_id: str, location: str, price: float, size: float, business_type: str):
        """
        Set the details of the premise for rent
        """
        self.premise_id = premise_id
        self.location = location
        self.price = price
        self.size = size
        self.business_type = business_type
        
    def create_premise_offer(self) -> Dict[str, Any]:
        """
        Create an offer for the premise
        """
        protocol = self.get_protocol("PremiseOffer")
        if protocol:
            return protocol.create_offer_message(
                self.premise_id,
                self.location,
                self.price,
                self.size,
                self.business_type
            )
        return {}
        
    def cancel_offer(self):
        """
        Cancel the current premise offer
        """
        print(f"{self.agent_name} cancelling premise offer")
        # In a real implementation, this would send a cancellation message
        return True