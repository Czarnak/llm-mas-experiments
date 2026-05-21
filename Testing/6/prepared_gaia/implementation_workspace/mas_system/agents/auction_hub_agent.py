from .base_agent import BaseAgent
from mas_system.protocols.premise_offer_protocol import PremiseOfferProtocol
from mas_system.protocols.tenant_offer_protocol import TenantOfferProtocol
from mas_system.protocols.service_demand_protocol import ServiceDemandProtocol
from mas_system.protocols.decision_protocol import DecisionProtocol
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from typing import Dict, Any, List


class AuctionHubBehaviour(CyclicBehaviour):
    """
    Behaviour for AuctionHub agent
    """
    
    async def run(self):
        # This is a simplified version - in a real system, this would handle
        # receiving messages and coordinating matches
        msg = await self.receive(timeout=10)
        if msg:
            print(f"AuctionHub received: {msg.body}")
            # Process the message based on protocol
            protocol_type = msg.get_metadata("protocol")
            if protocol_type == "PremiseOffer":
                protocol = self.agent.get_protocol("PremiseOffer")
                if protocol:
                    result = protocol.process_message(eval(msg.body))
                    if result:
                        # Send response
                        response = Message(to=msg.sender, body=str(result))
                        response.set_metadata("protocol", "PremiseOffer")
                        await self.send(response)
            elif protocol_type == "TenantOffer":
                protocol = self.agent.get_protocol("TenantOffer")
                if protocol:
                    result = protocol.process_message(eval(msg.body))
                    if result:
                        # Send response
                        response = Message(to=msg.sender, body=str(result))
                        response.set_metadata("protocol", "TenantOffer")
                        await self.send(response)


class AuctionHubAgent(BaseAgent):
    """
    Agent representing the Auction Hub that coordinates matches
    """
    
    def __init__(self, jid: str, password: str, agent_name: str):
        super().__init__(jid, password, agent_name)
        self.premises = {}
        self.tenants = {}
        self.service_demands = {}
        self.matching_results = {}
        
    async def setup(self):
        await super().setup()
        
        # Add protocols
        premise_protocol = PremiseOfferProtocol()
        self.add_protocol("PremiseOffer", premise_protocol)
        
        tenant_protocol = TenantOfferProtocol()
        self.add_protocol("TenantOffer", tenant_protocol)
        
        service_protocol = ServiceDemandProtocol()
        self.add_protocol("ServiceDemandRequest", service_protocol)
        
        decision_protocol = DecisionProtocol()
        self.add_protocol("DecideOffer", decision_protocol)
        
        # Add behaviours
        behaviour = AuctionHubBehaviour()
        self.add_behaviour(behaviour)
        
    def register_premise(self, premise_id: str, location: str, price: float, size: float, business_type: str) -> bool:
        """
        Register a premise for auction
        """
        self.premises[premise_id] = {
            'location': location,
            'price': price,
            'size': size,
            'business_type': business_type,
            'status': 'active'
        }
        print(f"Registered premise {premise_id} at {location}")
        return True
        
    def register_tenant(self, tenant_id: str, business_type: str, preferred_location: str, max_price: float) -> bool:
        """
        Register a tenant for matching
        """
        self.tenants[tenant_id] = {
            'business_type': business_type,
            'preferred_location': preferred_location,
            'max_price': max_price,
            'status': 'active'
        }
        print(f"Registered tenant {tenant_id}")
        return True
        
    def process_service_demand(self, citizen_id: str, service_type: str, location: str, priority: str = "medium") -> bool:
        """
        Process a service demand from a citizen
        """
        self.service_demands[citizen_id] = {
            'service_type': service_type,
            'location': location,
            'priority': priority
        }
        print(f"Processed service demand from citizen {citizen_id} for {service_type}")
        return True
        
    def match_premises_and_tenants(self) -> Dict[str, Any]:
        """
        Match premises with tenants based on criteria
        """
        # Simplified matching logic - in a real system this would be more complex
        matches = {}
        
        for premise_id, premise_info in self.premises.items():
            for tenant_id, tenant_info in self.tenants.items():
                # Simple matching based on business type and location proximity
                if premise_info['business_type'] == tenant_info['business_type']:
                    matches[f"{premise_id}_{tenant_id}"] = {
                        'premise_id': premise_id,
                        'tenant_id': tenant_id,
                        'premise_info': premise_info,
                        'tenant_info': tenant_info,
                        'match_score': 1.0  # Simplified scoring
                    }
        
        self.matching_results = matches
        print(f"Generated {len(matches)} matches")
        return matches
        
    def get_matching_results(self) -> Dict[str, Any]:
        """
        Get the matching results
        """
        return self.matching_results
        
    def cancel_premise_offer(self, premise_id: str) -> bool:
        """
        Cancel a premise offer
        """
        if premise_id in self.premises:
            self.premises[premise_id]['status'] = 'cancelled'
            print(f"Cancelled premise offer {premise_id}")
            return True
        return False
        
    def get_premises(self) -> Dict[str, Any]:
        """
        Get all registered premises
        """
        return self.premises
        
    def get_tenants(self) -> Dict[str, Any]:
        """
        Get all registered tenants
        """
        return self.tenants