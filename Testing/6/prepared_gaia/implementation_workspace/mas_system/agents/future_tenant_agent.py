from .base_agent import BaseAgent
from mas_system.protocols.tenant_offer_protocol import TenantOfferProtocol
from mas_system.protocols.decision_protocol import DecisionProtocol
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from typing import Dict, Any


class FutureTenantBehaviour(CyclicBehaviour):
    """
    Behaviour for FutureTenant agent
    """
    
    async def run(self):
        # This is a simplified version - in a real system, this would handle
        # receiving messages and responding appropriately
        msg = await self.receive(timeout=10)
        if msg:
            print(f"FutureTenant received: {msg.body}")
            # Process the message
            protocol = self.agent.get_protocol("TenantOffer")
            if protocol:
                result = protocol.process_message(eval(msg.body))
                if result:
                    # Send response
                    response = Message(to=msg.sender, body=str(result))
                    response.set_metadata("protocol", "TenantOffer")
                    await self.send(response)


class FutureTenantAgent(BaseAgent):
    """
    Agent representing a future tenant
    """
    
    def __init__(self, jid: str, password: str, agent_name: str):
        super().__init__(jid, password, agent_name)
        self.tenant_id = None
        self.business_type = None
        self.preferred_location = None
        self.max_price = None
        
    async def setup(self):
        await super().setup()
        
        # Add protocols
        tenant_protocol = TenantOfferProtocol()
        self.add_protocol("TenantOffer", tenant_protocol)
        
        decision_protocol = DecisionProtocol()
        self.add_protocol("DecideOffer", decision_protocol)
        
        # Add behaviours
        behaviour = FutureTenantBehaviour()
        self.add_behaviour(behaviour)
        
    def set_tenant_details(self, tenant_id: str, business_type: str, preferred_location: str, max_price: float):
        """
        Set the details of the future tenant
        """
        self.tenant_id = tenant_id
        self.business_type = business_type
        self.preferred_location = preferred_location
        self.max_price = max_price
        
    def create_tenant_offer(self, premise_id: str) -> Dict[str, Any]:
        """
        Create an offer as a tenant
        """
        protocol = self.get_protocol("TenantOffer")
        if protocol:
            return protocol.create_offer_message(
                self.tenant_id,
                premise_id,
                self.max_price,
                self.preferred_location,
                self.business_type
            )
        return {}
        
    def make_bid(self, premise_id: str, bid_amount: float) -> Dict[str, Any]:
        """
        Make a bid on a premise
        """
        print(f"{self.agent_name} making bid of {bid_amount} for premise {premise_id}")
        # In a real implementation, this would send the bid to the AuctionHub
        return {
            'tenant_id': self.tenant_id,
            'premise_id': premise_id,
            'bid_amount': bid_amount,
            'status': 'bid_placed'
        }